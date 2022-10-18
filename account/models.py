
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    roles = (
        ('admin', 'ADMIN'),
        ('teacher', 'TEACHER')
    )

<<<<<<< HEAD
    role = models.CharField(choices=roles, max_length=100)



=======
    role = models.CharField(choices=roles, max_length=50)
>>>>>>> 44ef7d22a0f2a74ccf4ecb0fa9e8e14966389306
