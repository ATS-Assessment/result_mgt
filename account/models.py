
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


class User(AbstractUser):
    roles = (
        ('admin', 'ADMIN'),
        ('teacher', 'TEACHER')
    )

    username = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(_('email address'), max_length=150, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(choices=roles, max_length=100)
    objects = UserManager()

    def get_all_teacher(self):
        return User.objects.all().exclude(role='admin')

    def __str__(self):
        return str(self.full_name)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS = ['full_name']
