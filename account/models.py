
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    roles = (
        ('admin', 'ADMIN'),
        ('teacher', 'TEACHER')
    )

    role = models.CharField(choices=roles, max_length=100)

