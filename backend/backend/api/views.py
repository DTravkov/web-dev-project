
from django.db import transaction
from django.db.models import Count
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import JsonResponse as JSONResponse
import json

from .serializers import CommentSerializer, DisciplineSerializer, PendingDisciplineSerializer, UserSerializer
from .models import Discipline, Comment, PendingDiscipline
from .permissions import IsCommentOwner
from .constants import MANAGER

@api_view(http_method_names=['GET'])
def is_moderator(request):
    if request.user.is_superuser:
        return Response({"detail" : "admin"}, status=status.HTTP_200_OK)
    if request.user.groups.filter(name='Manager').exists():
        return Response({"detail" : "manager"}, status=status.HTTP_200_OK)
    return Response({"detail" : "user"}, status=status.HTTP_200_OK)


class NoUpdateModelViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    pass

class PendingDisciplineViewSet(NoUpdateModelViewSet):
    queryset = PendingDiscipline.objects.all()
    serializer_class = PendingDisciplineSerializer
    def get_serializer(self, *args, **kwargs):
        if self.action == 'approve':
            return None
        return super().get_serializer(*args, **kwargs)
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(methods=['POST'], detail=True)
    def approve(self, request, pk):
        record = self.get_object()
        record_data = PendingDisciplineSerializer(record).data
        record_data.pop('id', None)
        with transaction.atomic():
            Discipline.objects.create(**record_data, approved_by=request.user)
            record.delete()

        return Response({"detail" : "Successfully approved"},status=status.HTTP_201_CREATED)

class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.select_related('approved_by').annotate(comment_count=Count('comments'))


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def get_serializer_class(self):
        if self.action == 'comments':
            return CommentSerializer
        return DisciplineSerializer
    

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'comments']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def perform_create(self, serializer):
        return serializer.save(approved_by=self.request.user)
    
    @action(methods=['GET'], detail=True)
    def comments(self, request, pk):
        discipline = self.get_object()
        comments = discipline.comments.select_related('author').annotate(
            likes_count=Count('likes' , distinct=True),
            dislikes_count=Count('dislikes', distinct=True)).all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentViewSet(NoUpdateModelViewSet):
    queryset = Comment.objects.select_related('author', 'discipline').all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminUser()]
        if self.action in ['list', 'retrieve', 'comment_detail']:
            return [AllowAny()]
        if self.action in ['create', 'like', 'dislike']:
            return [IsAuthenticated()]
        return [IsAuthenticated(),IsCommentOwner()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    
    @action(methods=['GET'], detail=True)
    def comment_detail(self, request, pk):
        try:
            comment_cache = f'comment:{pk}'
            comment = cache.get(comment_cache)
            if comment is not None:
                serializer = self.get_serializer(comment)
            else:
                queryset = Comment.objects.annotate(
                likes_count=Count('likes', distinct=True),
                dislikes_count=Count('dislikes', distinct=True)
            )
                comment = queryset.get(pk=pk)                
                serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(methods = ['GET'],detail= True)
    def redis_test_get(self,request,pk):
        cache_key = 'value'
        cache.set(cache_key,1000,timeout=5000)
        return JSONResponse({"value" : cache.get('comment_1_cache')})
    



    @action(methods=['POST'],detail = True)
    def like(self,request, pk):
        with transaction.atomic():
            comment = Comment.objects.get(pk=pk)
            user = self.request.user

            if comment.likes.filter(id=user.id).exists():
                comment.likes.remove(user)
            else:
                comment.likes.add(user)
                comment.dislikes.remove(user)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['POST'],detail = True)
    def dislike(self,request,pk):
        with transaction.atomic():
            comment = Comment.objects.get(pk=pk)
            user = self.request.user

            if  comment.dislikes.filter(id=user.id).exists():
                comment.dislikes.remove(user)
            else:
                comment.dislikes.add(user)
                comment.likes.remove(user)
            
            return Response(status=status.HTTP_204_NO_CONTENT)

    
    
class UserViewSet(NoUpdateModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=True, methods=['post'], permission_classes = [IsAdminUser])
    def ban(self,request, pk = None):
        user = self.get_object()

        if user == request.user:
            return Response({"detail" : f"can not to ban yourself" },status=status.HTTP_200_OK)
        
        user.is_active = False
        user.save()

        return Response({"detail" : f"user {user.username}, id : {user.id} banned"},status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['post'], permission_classes = [IsAdminUser])
    def unban(self,request, pk = None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"detail" : f"user {user.username}, id : {user.id} banned"},status = status.HTTP_200_OK)
        


    
    
