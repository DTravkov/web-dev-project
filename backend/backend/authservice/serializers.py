from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    username = serializers.CharField(required=True, validators=[UniqueValidator(User.objects.all(), "This username is already taken.")])
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True)

class CustomRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except TokenError as e:
            raise serializers.ValidationError('Invalid/blacklisted token.')
        except Exception as e:
            raise serializers.ValidationError('Error while refreshing the token')

class CheckSerializer(serializers.Serializer):
    access = serializers.CharField(required=True)
    refresh = serializers.CharField(required=True)