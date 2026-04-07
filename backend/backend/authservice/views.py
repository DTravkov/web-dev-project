from rest_framework import status, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer, LogoutSerializer, SignUpSerializer, CustomRefreshSerializer, CheckSerializer



class AuthViewSet(GenericViewSet):

    def get_serializer_class(self, *args, **kwargs):
        serializer_map = {
            'signup' : SignUpSerializer,
            'login' : LoginSerializer,
            'logout' : LogoutSerializer,
            'refresh' : CustomRefreshSerializer
        }
        option = serializer_map.get(self.action, None)
        if option is not None:
            return option
        
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action in ['refresh', 'logout']:
            return [IsAuthenticated()]
        
        return [AllowAny()]
    
    @action(detail=False, methods=['POST'])
    def logout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.validated_data.get('refresh', None))
            token.blacklist()
        except TokenError:
            raise APIException("Invalid token provided", code=status.HTTP_401_UNAUTHORIZED)


        return Response({"detail" : "Successful logout"}, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = RefreshToken.for_user(serializer.validated_data['user'])
        access = refresh.access_token

        return Response( { "refresh" : str(refresh),
                           "access" : str(access) }, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response( { "refresh" : str(refresh),
                           "access" : str(access) }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data.get('refresh')
        access = serializer.validated_data.get('access')
        
        return Response({"refresh" : str(refresh), "access" : str(access) }, status=status.HTTP_200_OK)