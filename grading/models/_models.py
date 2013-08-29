from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.

class NamedSortable(models.Model):

    name = models.CharField("Object name", max_length=100)
    sort_key = models.CharField("Sort key", max_length=100)

    class Meta:
        abstract = True
        ordering = ("sort_key",)

class Student(models.Model):

    user = models.ForeignKey("auth.User")
    group = models.ForeignKey("StudentGroup", related_name="students", null=True, blank=True)


class StudentGroup(NamedSortable):
    pass


class GradeableActivity(NamedSortable):
    group = models.ForeignKey("StudentGroup", related_name="activities", null=True, blank=True)


class GradePart(NamedSortable):

    weight = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)
    required = models.BooleanField("Is activity required")
    activity = models.ForeignKey("GradeableActivity")


class PartialGrade(models.Model):

    grade = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)
    student = models.ForeignKey("Student")
    grade_part = models.ForeignKey("GradePart")

    short_description = models.CharField("Short description", max_length=100)
    long_description = models.TextField("Long description")


class StudentGrade(models.Model):
    student = models.ForeignKey("Student")
    activity = models.ForeignKey("GradeableActivity")

    grade = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)


