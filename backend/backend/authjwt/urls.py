from rest_framework import routers

from .views import SignupViewSet

auth_router = routers.DefaultRouter()
auth_router.register("api", SignupViewSet, 'signup')