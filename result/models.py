from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.shortcuts import redirect

# Create your models here.

SESSIONS = (
    ('2022/2023', '2022/2023'),
    ('2023/2024', '2023/2024'),
    ('2024/2025', '2024/2025'),
    ('2025/2026', '2025/2026'),
    ('2026/2027', '2026/2027'),
)


class DeletedResultManager(models.Manager):

    def get_queryset(self):
        return Result.objects.filter(is_inactive=True)


class ActiveResultManager(models.Manager):

    def get_queryset(self):
        return Result.objects.filter(is_inactive=False)


class Result(models.Model):
    TERM = (
        ('first_term', 'First Term'),
        ('second_term', 'Second Term'),
        ('third_term', 'Third Term')
    )
    classes = models.ForeignKey('klass.Klass', on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=255)
    term = models.CharField(choices=TERM, max_length=255, null=True)
    session = models.CharField(max_length=10, choices=SESSIONS)
    position = models.IntegerField()
    scores = models.ForeignKey('Score', on_delete=models.CASCADE, null=True)
    current_teacher = models.ForeignKey(
        'account.User', null=True, on_delete=models.CASCADE)
    minimum_subjects = models.IntegerField()
    number_of_subjects_taken = models.IntegerField()
    number_of_passes = models.IntegerField()
    number_of_failures = models.IntegerField()
    minimum_marks = models.IntegerField()
    marks_obtained = models.IntegerField()
    term_average = models.IntegerField()
    comment = models.TextField(max_length=255, null=True, blank=True)
    is_inactive = models.BooleanField(default=False)
    is_not_student = models.BooleanField(default=False)
    guardian_email = models.EmailField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    deleted_results = DeletedResultManager()
    active_results = ActiveResultManager()

    def __str__(self):
        return self.student_name + " - " + str(self.classes) + f"({self.session})"

    def get_absolute_url(self):
        return redirect('index')


class Token(models.Model):
    count = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    result = models.ForeignKey(
        Result, on_delete=models.CASCADE, null=True, blank=True)
    token = models.CharField(max_length=10)


class Score(models.Model):
    # GRADES = (
    #     ('A1', 'A1'),
    #     ('B2', 'B2'),
    #     ('B3', 'B3'),
    #     ('C4', 'C4'),
    #     ('C5', 'C5'),
    #     ('C6', 'C6'),
    #     ('D7', 'D7'),
    #     ('E8', 'E8'),
    #     ('F9', 'F9')
    # )

    REMARKS = (
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('poor', 'Poor'),
        ('very_poor', 'Very Poor')
    )

    test_one = models.IntegerField(validators=[MaxValueValidator(10)])
    test_two = models.IntegerField(validators=[MaxValueValidator(10)])
    quiz = models.IntegerField(validators=[MaxValueValidator(5)])
    assignment = models.IntegerField(validators=[MaxValueValidator(5)])
    exam = models.IntegerField(validators=[MaxValueValidator(70)])
    # grade = models.CharField(choices=GRADES, null=True, blank=True)
    highest_in_class = models.IntegerField()
    lowest_in_class = models.IntegerField()
    remarks = models.CharField(
        choices=REMARKS, max_length=255, null=True, blank=True)

    @property
    def total_mark(self):
        return self.test_one + self.test_two +\
            self.quiz + self.assignment + self.exam

    @property
    def grade(self):
        if self.total_mark >= 75:
            return 'A1'
        if 70 <= self.total_mark <= 74:
            return 'B2'
        if 65 <= self.total_mark <= 69:
            return 'B3'
        if 60 <= self.total_mark <= 64:
            return 'C4'
        if 55 <= self.total_mark <= 59:
            return 'C5'
        if 50 <= self.total_mark <= 54:
            return 'C6'
        if 45 <= self.total_mark <= 49:
            return 'D7'
        if 40 <= self.total_mark <= 44:
            return 'E8'
        if 0 <= self.total_mark <= 39:
            return 'F9'

    # class Meta:
    #     ordering = ['-total_mark']
