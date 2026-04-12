from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import SignupSerializer



class SignupViewSet(GenericViewSet):
    serializer_class = SignupSerializer
    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail" : "Successfully signed up"} , status=status.HTTP_201_CREATED)
