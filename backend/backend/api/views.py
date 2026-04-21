
from django.db import transaction
from django.db.models import Count, Q
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticated
from django.contrib.auth.models import User

from .serializers import CommentSerializer, DisciplineSerializer, PendingDisciplineSerializer, PendingProfessorSerializer, ProfessorSerializer, UserProfileSerializer, UserSerializer
from .models import Discipline, Comment, PendingDiscipline, PendingProfessor, Professor
from .permissions import IsCommentOwner, IsModerator

@api_view(http_method_names=['GET'])
def is_moderator(request):
    if request.user.is_superuser:
        return Response({"detail" : "admin"}, status=status.HTTP_200_OK)
    if request.user.groups.filter(name='Manager').exists():
        return Response({"detail" : "manager"}, status=status.HTTP_200_OK)
    return Response({"detail" : "user"}, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def stats(request):

    return Response(
        {
            "users_count": User.objects.count(),
            "comments_count": Comment.objects.count(),
            "teachers_count": Professor.objects.count(),
            "disciplines_count": Discipline.objects.count(),
            "pending_count": PendingDiscipline.objects.count() + PendingProfessor.objects.count(),
        },
        status=status.HTTP_200_OK,
    )


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
        if self.action in ['create', 'mypending']:
            return [IsAuthenticated()]
        return [IsModerator()]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=True)
    def approve(self, request, pk):
        record = self.get_object()
        record_data = PendingDisciplineSerializer(record).data
        record_data.pop('id', None)
        with transaction.atomic():
            Discipline.objects.create(**record_data, approved_by=request.user)
            record.delete()

        return Response({"detail" : "Successfully approved"},status=status.HTTP_201_CREATED)
    
    @action(methods=['GET'], detail=False)
    def mypending(self, request):
        serializer = PendingDisciplineSerializer(self.queryset.filter(author_id=request.user.id), many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def allpending(self, request):
        serializer = PendingDisciplineSerializer(self.queryset.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PendingProfessorViewSet(NoUpdateModelViewSet):
    queryset = PendingProfessor.objects.select_related('discipline')
    serializer_class = PendingProfessorSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'approve':
            return None
        return super().get_serializer(*args, **kwargs)

    def get_permissions(self):
        if self.action in ['create', 'mypending']:
            return [IsAuthenticated()]
        return [IsModerator()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=True)
    def approve(self, request, pk):
        record = self.get_object()
        with transaction.atomic():
            Professor.objects.create(
                name=record.name,
                surname=record.surname,
                discipline=record.discipline,
            )
            record.delete()

        return Response({"detail": "Successfully approved"}, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def mypending(self, request):
        serializer = PendingProfessorSerializer(self.queryset.filter(author_id=request.user.id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def allpending(self, request):
        serializer = PendingProfessorSerializer(self.queryset.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.select_related('approved_by').prefetch_related('professors_list').annotate(comment_count=Count('comments'))

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
        comments = discipline.comments.annotate(
            likes_count=Count('likes'),
            dislikes_count=Count('dislikes')).select_related('author')
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
            queryset = Comment.objects.annotate(
                likes_count=Count('likes', distinct=True),
                dislikes_count=Count('dislikes', distinct=True)
            )
            comment = queryset.get(pk=pk) 
            
            serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)


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
    def get_queryset(self):
        if self.action in ['retrieve', 'profile']:
            return User.objects.all().annotate(
                comment_count=Count('user_comments', distinct=True),
                like_count=Count('user_comments__likes', filter=Q(user_comments__likes__isnull=False), distinct=True),
                dislike_count=Count('user_comments__dislikes', filter=Q(user_comments__dislikes__isnull=False), distinct=True),
            )
        return User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'profile':
            return UserProfileSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve', 'profile']:
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

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def profile(self, request, pk = None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfessorViewSet(NoUpdateModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    @action(methods=['GET'], detail=True)
    def comments(self, request,pk):
        professor = self.get_object()
        queryset = professor.professor_comments.all().select_related('author', 'discipline')
    
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
