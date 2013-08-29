from django.db import models

# Create your models here.

class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = "grading"

class NamedSortable(models.Model):

    name = models.CharField("Object name", max_length=100)
    sort_key = models.CharField("Sort key", max_length=100)

    class Meta:
        abstract = True
        app_label = "grading"
        ordering = ("sort_key",)

class Student(BaseModel):

    user = models.ForeignKey("auth.User")
    group = models.ForeignKey("StudentGroup", related_name="students", null=True, blank=True)


class StudentGroup(NamedSortable):
    pass


class GradeableActivity(NamedSortable):
    groups = models.ManyToManyField("StudentGroup", related_name="activities")


class GradePart(NamedSortable):

    weight = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)
    required = models.BooleanField("Is activity required")
    activity = models.ForeignKey("GradeableActivity")


class PartialGrade(BaseModel):

    grade = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)
    student = models.ForeignKey("Student")
    grade_part = models.ForeignKey("GradePart")

    short_description = models.CharField("Short description", max_length=100)
    long_description = models.TextField("Long description")


class StudentGrade(BaseModel):
    student = models.ForeignKey("Student", related_name="grades")
    activity = models.ForeignKey("GradeableActivity")

    grade = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)


