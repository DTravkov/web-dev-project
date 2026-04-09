from rest_framework import serializers, status
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from rest_framework.validators import UniqueValidator


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(User.objects.all(), message="This username is already in use.")])
    password = serializers.CharField(required=True, write_only=True)

    def validate_username(self,value):
        if len(value) < 2 or len(value) > 40:
            raise serializers.ValidationError(detail="Username must consist of (3-40) characters", code=status.HTTP_400_BAD_REQUEST)
        return value

    
    def validate_password(self,value):
        password_validation.validate_password(value)
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],password=validated_data['password'])
        return user

