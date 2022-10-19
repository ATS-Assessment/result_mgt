
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string


# Create your models here.


def _subject_json():
    return list


def _previous():
    return list


# def generate_token():
#     return "".join(random.choices(string.ascii_lowercase + string.digits, k=7))


class Klass(models.Model):
    SESSION_CHOICES = (
        ("First term", "First term"),
        ("Second term", "Second term"),
        ("Third term", "Third term"),
    )
    name = models.CharField(max_length=100)
    no_of_students = models.IntegerField()
    subject = models.JSONField(default=_subject_json)
    teacher = models.ForeignKey("account.User", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.CharField(choices=SESSION_CHOICES, max_length=100)
    year = models.DateTimeField()
    token = models.CharField(max_length=30, default=generate_token)
    previous_teachers = models.JSONField(default=__previous)

    def __str__(self) -> str:
        return self.name

    birthday = models.DateTimeField()

    def get_year(self):
        return self.year.year
