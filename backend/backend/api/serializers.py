
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import serializers, status

from .models import PendingDiscipline, Discipline, Comment, Professor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields = ['id', 'username']

class PendingDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingDiscipline
        fields = ('id','name')
    def validate_name(self, value:str):
        if Discipline.objects.filter(name=value).exists():
            raise serializers.ValidationError("Discipline with that name already exists", code=status.HTTP_409_CONFLICT)
        return value.strip()
    
    
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    rating = serializers.IntegerField(required=True)
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id','discipline','author', 'author_avatar', 'content', 'rating', 'created_at', 'likes_count', 'dislikes_count', 'professor')
        read_only_fields = ['author', 'author_avatar', 'created_at', 'likes_count', 'dislikes_count']

    def validate_rating(self,value):
        if value > 5 or value < 1:
            raise serializers.ValidationError("Rating must be in range (1-5)")
        return value
    
    def get_author_avatar(self, obj):
        profile = obj.author.profile
        return profile.avatar.url if profile and profile.avatar else None
        

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('__all__')

class DisciplineSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)
    professors_list = ProfessorSerializer(many=True, read_only=True)
    class Meta:
        model = Discipline
        fields = ('id','name', 'created_at','approved_by', 'comment_count', 'professors_list')
        read_only_fields = ['created_at', 'approved_by', 'professors_list', 'comment_count']


class ApprovedDisciplineSerializer(serializers.Serializer):
       class Meta:
        model = Discipline
        fields = ('id','name', 'created_at','approved_by', 'comments')
        read_only_fields = ['id','name', 'created_at','approved_by', 'comments']
    

