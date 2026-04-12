from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def check_manager_permissions(user: User):
    return user.is_active and (user.is_superuser or user.groups.filter(name="Manager").exists() or user.groups.filter(name="manager").exists())
