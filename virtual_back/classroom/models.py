from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
# models.py
from django.contrib.auth.models import User

class Class(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructed_classes")

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="enrollments")

    def __str__(self):
        return f"{self.student.username} enrolled in {self.classroom.name}"


class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)

class Class(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')

class Unit(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=100)

class Session(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=100)

class Lecture(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='lectures')
    content = models.TextField()

class Comment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
