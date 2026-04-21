
from rest_framework import routers
from django.urls import path

from .views import CommentViewSet, DisciplineViewSet, PendingDisciplineViewSet, PendingProfessorViewSet, ProfessorViewSet, UserViewSet, stats

api_router = routers.DefaultRouter()
api_router.register('api/disciplines', DisciplineViewSet, basename='discipline')
api_router.register('api/comments', CommentViewSet, basename='comment')
api_router.register('api/pending', PendingDisciplineViewSet, basename='pending')
api_router.register('api/pending-professors', PendingProfessorViewSet, basename='pending-professors')
api_router.register('api/users', UserViewSet, basename= 'users')
api_router.register('api/professors', ProfessorViewSet, basename= 'professors')

urlpatterns = [
    path('api/stats/', stats, name='stats'),
]
