from django.db import models

# Create your models here.

__all__ = ['Student', 'StudentGrade', 'StudentGroup', 'GradeableActivity', 'GradePart', 'PartialGrade']

class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = "grading"

class NamedSortable(models.Model):

    """
    Class representing something that has :attr:`name` and :attr:`sort_key`
    """

    name = models.CharField("Object name", max_length=100, null=False, blank=False, unique=True)
    sort_key = models.CharField("Sort key", max_length=100, null=False, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        app_label = "grading"
        ordering = ("sort_key",)

class Student(BaseModel):
    """
    Represents a person that can be graded. By default all newly created users get
    a :class:`Student` counterpart (to disable it you need to modify
    :attr:`grading.models._signals.on_user_create`.
    """

    user = models.OneToOneField("auth.User")
    group = models.ForeignKey("StudentGroup", related_name="students", null=True, blank=True)

    class Meta:
        abstract = False
        app_label = "grading"
        ordering = ("user__last_name", "user__first_name", "user__email", "user__pk")


class StudentGroup(NamedSortable):
    """
    Group of students. Groups can be assigned :class:`.GradeableActivity`, for
    each of these activities students will get grades.
    """
    pass


class GradeableActivity(NamedSortable):

    """
    :class:`.GradeableActivity` consist of set of tasks, that are each graded
    separately, then weighted averatge is calculated. These tasks are represented
    by :class:`GradePart` instances.

    Relation between :class:`GradeableActivity` and :class:`Student` is through
    group in which student is registered.

    Grades are calculdated from the following formula:

    .. math::

        \frac{\sum w_i * g_i}{\sum w_i}

    Where :math:`w_i` are weights of partricular :class:`GradePart` and :math:`g_i`
    are grades for particular assigments.
    """

    groups = models.ManyToManyField("StudentGroup", related_name="activities")
    default_grade = models.DecimalField(
        "Default grade", max_digits=5, decimal_places=2,
        help_text="Grade used when some required activities are not finished",
        default=2.0)


class GradePart(NamedSortable):

    """
    Part of the grade.

    :attr:`weight`
        weight of grade.
    :attr:`default_grade`
        Grade that is used if student did not complete this task.
    :attr:`required`
        If true and stident did not completed this task, whole activity will
        be marked as not-done and student will get :attr:`.activity.default_grade`
    :attr:`activity`
        Activity this instance is attached to.
    """

    weight = models.DecimalField("Activity weight", max_digits=5, decimal_places=2)
    default_grade = models.DecimalField(
        "Default grade", max_digits=5, decimal_places=2,
        help_text="Grade used when student did not get partial grade for this GradePart",
        default=2.0)
    passing_grade = models.DecimalField(
        "Passing grade", max_digits=5, decimal_places=2,
        help_text="If grade is lower than passing grade we will assume this as not finished task",
        default=3.0)
    required = models.BooleanField("Is activity required")
    activity = models.ForeignKey("GradeableActivity", related_name="grade_parts")


class PartialGrade(BaseModel):

    """
    Grade for given :class:`.Student` for given :class:.GradePart. Apart from grade
    itself it contains short and long description fields.
    """

    grade = models.DecimalField("Activity weight", max_digits=5, decimal_places=2, null=False, blank=False)
    student = models.ForeignKey("Student")
    grade_part = models.ForeignKey("GradePart", null=False)

    short_description = models.CharField("Short description", max_length=100, null=True, blank=True)
    long_description = models.TextField("Long description", null=True, blank=True)


class StudentGrade(BaseModel):
    """
    Calculdated grade for given :class:`.Student` and :class:.GradeableActivity.
    This is automatically generated from :class:.PartialGrade.

    Grades get calculated to student if:

    * Student is added to group that contains activities (student will get grade
      for each activity)
    * Activity is added to group (all students will get grades for this activity)
    * Any :class:.PartialGrade is added/udated/deleted.
    """

    student = models.ForeignKey("Student", related_name="grades")
    activity = models.ForeignKey("GradeableActivity")

    grade = models.DecimalField("Grade", max_digits=5, decimal_places=2)


