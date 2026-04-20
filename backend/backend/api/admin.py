from django.contrib import admin

from .models import Comment, Discipline, PendingDiscipline, Professor, Profile


admin.site.register([Discipline, PendingDiscipline, Comment, Profile, Professor])
