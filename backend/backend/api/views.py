
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, generics

from .serializers import CommentSerializer, DisciplineSerializer, PendingDisciplineSerializer
from .models import Discipline, Comment, PendingDiscipline
from .permissions import IsCommentOwner





class PendingDisciplineViewSet(viewsets.ModelViewSet):
    queryset = PendingDiscipline.objects.all()
    serializer_class = PendingDisciplineSerializer

    def get_permissions(self):
        if self.action in 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(methods=['POST'], detail=True)
    def approve(self, request, pk):
        record = self.get_object()
        record_data = PendingDisciplineSerializer(record).data
        record_data.pop('id', None)

        serializer = DisciplineSerializer(data=record_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(approved_by=request.user)
        record.delete()

        return Response(status=status.HTTP_201_CREATED)

class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.prefetch_related('comments__author').all()
    serializer_class = DisciplineSerializer

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def perform_create(self, serializer):
        return serializer.save(approved_by=self.request.user)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'discipline').all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.user.is_staff :
            return [permissions.IsAdminUser()]
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(),IsCommentOwner()]

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Comments cannot be edited"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    
