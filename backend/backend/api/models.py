from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def build_avatar_path(instance, filename):
    return f'avatars/{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = ProcessedImageField(
        upload_to=build_avatar_path,
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 80},
        default='avatars/default.png',
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.user}'s profile"

    

class PendingDiscipline(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, unique=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_pending')
    def __str__(self):
        return f"{self.name}"


class PendingProfessor(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    surname = models.CharField(max_length=20, null=False, blank=False)
    discipline = models.ForeignKey(
        'Discipline',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pending_professors',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_pending_professors')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'surname', 'discipline'],
                name='unique_pending_professor_per_discipline',
            )
        ]

    def __str__(self):
        return f"{self.name} {self.surname}"

    
class Professor(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    surname = models.CharField(max_length=20, null=False, blank=False)
    discipline = models.ForeignKey(
        'Discipline', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='professors_list'
    )

    def __str__(self):
        return f"{self.name} {self.surname}"
    
class Discipline(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User,on_delete=models.PROTECT, related_name='approved_by')
    def __str__(self):
        return f"{self.name}"
    
class Comment(models.Model):
    content = models.TextField(max_length=1000, null=False, blank=False)
    rating = models.IntegerField(null=False,blank=False, choices=[(1,"1"), (2,"2"), (3,"3"), (4,"4"), (5,"5")])
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments',blank = True)
    dislikes = models.ManyToManyField(User,related_name='disliked_comments',blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='comments')
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='professor_comments')

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_dislikes(self):
        return self.dislikes.count()
    

    def __str__(self):
        return f"{self.author.get_username()}, {self.discipline.name} : {self.content[:30]}"
    
