from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models

# Create your models here.
SESSIONS = (
    ('2022/2023', '2022/2023'),
    ('2023/2024', '2023/2024'),
    ('2024/2025', '2024/2025'),
    ('2025/2026', '2025/2026'),
    ('2026/2027', '2026/2027'),
)


class Result(models.Model):
    classes = models.ForeignKey('klass.Klass', on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=255)
    session = models.CharField(max_length=10, choices=SESSIONS)
    position = models.IntegerField()
    subjects = models.ManyToManyField('klass.Subject', related_name='results')
    current_teacher = models.ForeignKey('account.User', null=True, on_delete=models.CASCADE)
    minimum_subjects = models.IntegerField()
    number_of_subjects_taken = models.IntegerField()
    number_of_passes = models.IntegerField()
    number_of_failures = models.IntegerField()
    minimum_marks = models.IntegerField()
    marks_obtained = models.IntegerField()
    term_average = models.IntegerField()
    comment = models.CharField(max_length=255, null=True, blank=True)
    is_inactive = models.BooleanField(default=False)
    is_not_student = models.BooleanField(default=False)
    guardian_email = models.EmailField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Token(models.Model):
    count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=10)
