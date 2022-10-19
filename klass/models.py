
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
<<<<<<< HEAD
    no_of_students = models.IntegerField()
    subject = models.JSONField(default=_subject_json())
=======
    no_of_students = models.PositiveIntegerField(validators=[MinValueValidator(0),
                                                             MaxValueValidator(40)])
    # subject = models.JSONField(default=_subject_json)
>>>>>>> 19cc6f99a844e8d4d3f2cb94d4b489002d67fa75
    teacher = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.CharField(choices=SESSION_CHOICES, max_length=100)
    year = models.DateTimeField()
    # token = models.CharField(max_length=30, default=generate_token)
<<<<<<< HEAD
    previous_teachers = models.JSONField(default=_previous())
=======
    # previous_teachers = models.JSONField(default=_previous)
>>>>>>> 19cc6f99a844e8d4d3f2cb94d4b489002d67fa75

    def __str__(self) -> str:
        return self.name

    # def get_year(self):
    #     return self.year.year


class Subject(models.Model):
    LEVEL = (
        ("JUNIOR", "JUNIOR"),
        ("SENIOR", "SENIOR")
    )
    name = models.CharField(max_length=50)
    level = models.CharField(choices=LEVEL, max_length=50)

    def __str__(self) -> str:
        return self.name
