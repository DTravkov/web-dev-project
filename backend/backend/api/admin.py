from django.contrib import admin

from .models import Comment, Discipline, PendingDiscipline


admin.site.register([Discipline, PendingDiscipline, Comment])
