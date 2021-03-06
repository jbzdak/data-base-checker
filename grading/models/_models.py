from celery.result import AsyncResult
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext

# Create your models here.
from django.db.models.manager import Manager
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from grading.autograding import get_autograders
from picklefield.fields import PickledObjectField
from grading.autograding._base import GradingResult

__all__ = [
    'Student', 'StudentGrade', 'Course',
    'GradeableActivity', 'GradePart', 'PartialGrade',
    'AutogradeableGradePart', 'AutogradedActivity',
    'AutogradingResult']

class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = "grading"



class UniqueNamedSortable(models.Model):

    """
    Class representing something that has :attr:`name` and :attr:`sort_key`
    """

    name = models.CharField("Object name", max_length=100, null=False, blank=False, unique=True)
    sort_key = models.CharField("Sort key", max_length=100, null=False, blank=True)
    slug_field = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        app_label = "grading"
        ordering = ("sort_key",)

    def save(self, *args, **kwargs):
        if not self.sort_key:
            self.sort_key = self.name
        if not self.slug_field:
            self.slug_field = slugify(self.name)
        super().save(*args, **kwargs)

class NamedSortable(models.Model):

    """
    Class representing something that has :attr:`name` and :attr:`sort_key`
    """

    name = models.CharField("Object name", max_length=100, null=False, blank=False)
    sort_key = models.CharField("Sort key", max_length=100, null=False, blank=True)
    slug_field = models.SlugField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        app_label = "grading"
        ordering = ("sort_key",)

    def save(self, *args, **kwargs):
        if not self.sort_key:
            self.sort_key = self.name
        if not self.slug_field:
            self.slug_field = slugify(self.name)
        super().save(*args, **kwargs)

@python_2_unicode_compatible
class Student(BaseModel):
    """
    Represents a person that can be graded. By default all newly created users get
    a :class:`Student` counterpart (to disable it you need to modify
    :attr:`grading.models._signals.on_user_create`.
    """

    user = models.OneToOneField(
        "auth.User", related_name="student")
    student_id = models.CharField(
        max_length=100, unique=True, null=True)
    course = models.ForeignKey(
        "Course", related_name="students", null=True, blank=True)

    def __str__(self):
        if self.user.last_name:
            name_part = "{} {}".format(self.user.first_name, self.user.last_name)
        else:
            name_part = self.user.username
        return name_part

    class Meta:
        abstract = False
        app_label = "grading"
        ordering = ("user__last_name", "user__first_name", "user__email", "user__pk")


class Course(UniqueNamedSortable):
    """
    Group of students. Groups can be assigned :class:`.GradeableActivity`, for
    each of these activities students will get grades.
    """
    pass

    def get_absolute_url(self):
        return reverse("student-course", args=[self.slug_field])



class GradeableActivity(NamedSortable):

    """
    :class:`.GradeableActivity` consist of set of tasks, that are each graded
    separately, then weighted averatge is calculated. These tasks are represented
    by :class:`GradePart` instances.

    Relation between :class:`GradeableActivity` and :class:`Student` is through
    course in which student is registered.

    Grades are calculdated from the following formula:

    .. math::

        \frac{\sum w_i * g_i}{\sum w_i}

    Where :math:`w_i` are weights of partricular :class:`GradePart` and :math:`g_i`
    are grades for particular assigments.
    """

    courses = models.ManyToManyField("Course", related_name="activities")
    default_grade = models.DecimalField(
        "Default grade", max_digits=5, decimal_places=2,
        help_text="Grade used when some required activities are not finished",
        default=2.0)

    may_be_autograded_to = models.DateTimeField(
        "May be autograded to", default=None, null=True, blank=True
    )

    class Meta:
        app_label = "grading"


class GradePartManager(Manager):

    def grade(self, grade_part, student, grade, short_message=None):
        partial_grade, __ = PartialGrade.objects.get_or_create(
            grade_part=grade_part,
            student=student,
            defaults = {
                "grade": grade
            }
        )
        partial_grade.grade=grade
        partial_grade.short_description = short_message
        partial_grade.save()
        return partial_grade

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

    weight = models.DecimalField("Activity weight", max_digits=5, decimal_places=2, default=1, blank=True)
    default_grade = models.DecimalField(
        "Default grade", max_digits=5, decimal_places=2,
        help_text="Grade used when student did not get partial grade for this GradePart",
        default=None)
    passing_grade = models.DecimalField(
        "Passing grade", max_digits=5, decimal_places=2,
        help_text="If grade is lower than passing grade we will assume this as not finished task",
        default=3.0)
    required = models.BooleanField("Is activity required", default=False)
    activity = models.ForeignKey("GradeableActivity", related_name="grade_parts")

    objects = GradePartManager()

    def save(self, *args, **kwargs):
        if self.default_grade is None :
            self.default_grade = self.activity.default_grade
        super().save(*args, **kwargs)


    class Meta:
        app_label = "grading"
        ordering = ["sort_key"]
        unique_together = [("activity", "name")]

class BasePartialGrade(BaseModel):


    grade = models.DecimalField("Activity weight", max_digits=5, decimal_places=2, null=False, blank=False)
    student = models.ForeignKey("Student")
    grade_part = models.ForeignKey("GradePart", null=False)

    save_date = models.DateTimeField(auto_now=True, null=True)

    short_description = models.TextField("Short description", null=True, blank=True)
    long_description = models.TextField("Long description", null=True, blank=True)

    class Meta:
        abstract = True
        app_label = "grading"
        ordering = ['save_date']


class PartialGrade(BasePartialGrade):

    """
    Grade for given :class:`.Student` for given :class:.GradePart. Apart from grade
    itself it contains short and long description fields.
    """

    class Meta:
        unique_together = ("student", "grade_part")
        app_label = "grading"
        ordering = ['save_date']

class AutogradingResult(BasePartialGrade):

    autograder_input_content_type = models.ForeignKey(ContentType, null=True, blank=True, editable=False)
    autograder_input_pk = models.PositiveIntegerField(null=True, blank=True, editable=False)
    autograder_input = GenericForeignKey('autograder_input_content_type', 'autograder_input_pk')

    grading_result = PickledObjectField(null=True)

    partial_grade = models.ForeignKey(PartialGrade, related_name="autogrades", null=False, blank=False)

    is_pending = models.BooleanField("Is autograding in progress", default=False)

    celery_task_id = PickledObjectField(null=True)

    is_current = models.BooleanField(default=True)

    def fill_empty(self, student_input):
        self.is_pending=True
        self.autograder_input = student_input
        self.grade = self.grade_part.default_grade
        self.short_description = ugettext("Grading in progress")

    def fill(self, student_input, grading_result=None):
        self.is_pending=False
        self.autograder_input = student_input
        self.grade = grading_result.grade
        self.short_description = grading_result.comment
        self.grading_result = grading_result

    def fill_grading_failed(self):
        gr = GradingResult(
            self.grade_part.default_grade,
            ugettext("Grading failed with micalleneus error. Please consult your instructor")
        )
        self.fill(None, gr)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.partial_grade
        except PartialGrade.DoesNotExist:
            self.partial_grade, __ = PartialGrade.objects.get_or_create(
                student = self.student,
                grade_part = self.grade_part
            )

        type(self).objects.filter(
            grade=self.grade, grade_part=self.grade_part, student=self.student
        ).update(is_current=False)
        super().save(force_insert, force_update, using, update_fields)


    @property
    def celery_task(self):
        return AsyncResult(self.celery_task_id)

class AutogradedActivity(GradeableActivity):

    class Meta:
        proxy = True
        app_label = "grading"

class AutogradeableGradePart(GradePart):

    parent = models.OneToOneField(GradePart, parent_link=True, related_name="autograde")

    autograding_controller = models.CharField(
        choices=[("1", "This should be autofilledd"), ("2", "This should be autofilledd")],
        max_length=1000)

    may_be_autograded_to = models.DateTimeField(
        "May be autograded to", default=None, null=True, blank=True
    )

    def __init__(self, *args, **kwargs):
        super(AutogradeableGradePart, self).__init__(*args, **kwargs)
        self._meta.get_field('name').blank = True
        self._meta.get_field('autograding_controller')._choices = [(name, name) for name in sorted(get_autograders().keys())]

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.autograding_controller

        if not self.pk and not self.may_be_autograded_to:
            self.may_be_autograded_to = self.activity.may_be_autograded_to

        super(AutogradeableGradePart, self).save(*args, **kwargs)


    @property
    def autograder(self):
        return get_autograders()[self.autograding_controller]


class StudentGrade(BaseModel):
    """
    Calculdated grade for given :class:`.Student` and :class:.GradeableActivity.
    This is automatically generated from :class:.PartialGrade.

    Grades get calculated to student if:

    * Student is added to course that contains activities (student will get grade
      for each activity)
    * Activity is added to course (all students will get grades for this activity)
    * Any :class:.PartialGrade is added/udated/deleted.
    """

    student = models.ForeignKey("Student", related_name="grades")
    activity = models.ForeignKey("GradeableActivity")
    grade = models.DecimalField("Grade", max_digits=5, decimal_places=2)

    short_description = models.TextField("Short description", null=True, blank=True)
    long_description = models.TextField("Long description", null=True, blank=True)

    @property
    def passed(self):
        return self.grade > self.activity.default_grade

