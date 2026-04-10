from django.db import models
from django.contrib.auth.models import User


class PendingDiscipline(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, unique=True)
    def __str__(self):
        return f"{self.name}"

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
    dislikes = models.ManyToManyField(User,related_name='dislaked_comments',blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
        return f"{self.author.get_username()}, {self.discipline.name} : {self.content[:30]}"
    
