
from django.db import transaction
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django.contrib.auth.models import User

from .serializers import CommentSerializer, DisciplineSerializer, PendingDisciplineSerializer, UserSerializer
from .models import Discipline, Comment, PendingDiscipline
from .permissions import IsCommentOwner



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
    queryset = Discipline.objects.prefetch_related('comments__author').all()

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
        serializer = self.get_serializer(Comment.objects.filter(discipline__id=pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentViewSet(NoUpdateModelViewSet):
    queryset = Comment.objects.select_related('author', 'discipline').all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.user.is_staff:
            return [IsAdminUser()]
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(),IsCommentOwner()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(methods=['POST'],detail = True)
    def like(self,request, pk):
        comment = self.get_object()
        user = self.request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
            comment.dislikes.remove(user)
        
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['POST'],detail = True)
    def islike(self,request,pk):
        comment = self.get_object()
        user = self.request.user

        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
        else:
            comment.dislikes.add(user)
            comment.likes.remove(user)
        
        return Response(status = status.HTTP_200_OK)
    
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], permission_classes = [IsAdminUser])
    def ban(self,request, pk = None):
        user = self.get_object()

        if user == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()

        return Response(status = status.HTTP_200_OK)
    
    @action(detail=True,methods=['post'], permission_classes = [IsAdminUser])
    def unban(self,request, pk = None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(status = status.HTTP_200_OK)
        


    
    
