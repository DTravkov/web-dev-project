
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
    

class DisciplineSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Discipline
        fields = ('id','name', 'created_at','approved_by', 'comments')
        read_only_fields = ['approved_by']
    





    