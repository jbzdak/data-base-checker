from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Student(models.Model):

    user = models.ForeignKey("auth.User")
    group = models.ForeignKey("StudentGroup", related_name="students", null=True, blank=True)


class StudentGroup(models.Model):

    name = models.CharField("Group name", max_length=100)

class GradeableActivity(models.Model):

    name = models.CharField("Activity", max_length=100)
    group = models.ForeignKey("StudentGroup", related_name="activities", null=True, blank=True)

class GradePart(models.Model):

    weight = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)
    required = models.BooleanField("Is activity required")
    activity = models.ForeignKey("GradeableActivity")

class PartialGrade(models.Model):

    grade = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)

    student = models.ForeignKey("Student")
    grade_part = models.ForeignKey("GradePart")


class Grade(models.Model):
    student = models.ForeignKey("Student")
    activity = models.ForeignKey("GradeableActivity")

@receiver(post_save, sender=User)
def on_user_create(instance, **kwargs):
    Student.objects.create(user=instance)

