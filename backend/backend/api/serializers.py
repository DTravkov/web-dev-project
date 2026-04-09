
from django.contrib.auth.models import User
from rest_framework import serializers, status

from .models import PendingDiscipline, Discipline, Comment



class PendingDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingDiscipline
        fields = ('id','name')
    def validate_name(self, value:str):
        if Discipline.objects.filter(name=value).exists():
            raise serializers.ValidationError("Discipline with that name already exists", code=status.HTTP_409_CONFLICT)
        return value.strip()
    
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','discipline', 'author', 'content', 'rating', 'created_at')
        read_only_fields = ['author', 'created_at']
    rating = serializers.IntegerField(required=True)
    def validate_rating(self,value):
        if value > 5 or value < 1:
            raise serializers.ValidationError("Rating must be in range (1-5)")
        return value

class DisciplineSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Discipline
        fields = ('id','name', 'created_at','approved_by', 'comments')
        read_only_fields = ['approved_by']

class ApprovedDisciplineSerializer(serializers.Serializer):
       class Meta:
        model = Discipline
        fields = ('id','name', 'created_at','approved_by', 'comments')
        read_only_fields = ['id','name', 'created_at','approved_by', 'comments']
    





    