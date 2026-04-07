
from rest_framework import routers

from .views import CommentViewSet, DisciplineViewSet, PendingDisciplineViewSet

router = routers.DefaultRouter()
router.register('api/disciplines', DisciplineViewSet, basename='discipline')
router.register('api/comments', CommentViewSet, basename='comment')
router.register('api/pending', PendingDisciplineViewSet, basename='pending')