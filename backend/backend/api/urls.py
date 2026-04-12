
from rest_framework import routers

from .views import CommentViewSet, DisciplineViewSet, PendingDisciplineViewSet, UserViewSet

api_router = routers.DefaultRouter()
api_router.register('api/disciplines', DisciplineViewSet, basename='discipline')
api_router.register('api/comments', CommentViewSet, basename='comment')
api_router.register('api/pending', PendingDisciplineViewSet, basename='pending')
api_router.register('api/users', UserViewSet, basename= 'users')