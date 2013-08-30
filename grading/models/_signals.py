# coding=utf-8

import logging
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save

from django.db.utils import ProgrammingError
from django.dispatch.dispatcher import receiver

from grading.models._models import *
from grading.models._models import NamedSortable
from grading.models._util_funcs import *

LOGGER = logging.getLogger(__name__)

__all__ = []

@receiver(post_save, sender=User)
def on_user_create(instance, **kwargs):
    try:
        if instance.is_active and not instance.is_staff and not kwargs.get('raw', False):
            Student.objects.get_or_create(user=instance)
    except ProgrammingError as e:
        print(e.message)
        if "does not exist" in e.args[0] and 'grading_student' in e.args[0]:
            LOGGER.warning("Adding user before tables for grading subsystem. Student model was not installed for this user.")


@receiver(pre_save)
def on_gradeable_activity_create(instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, NamedSortable) and not instance.sort_key:
            instance.sort_key = instance.name


@receiver(post_save, sender=GradeableActivity)
def when_activity_added_sync_grades_for_students_in_group(instance, **kwargs):
    if not kwargs.get('raw', False):
        sync_grades_for_activity(instance)

@receiver(post_save, sender=Student)
def when_student_is_saved_in_group_sync_grades(instance, **kwargs):
    if not kwargs.get('raw', False):
        if instance.group is not None:
            sync_grades_for_student(instance)

@receiver(post_save, sender=PartialGrade)
def when_partial_grade_is_saved_update_student_grade(instance, **kwargs):
    if not kwargs.get('raw', False):
        sync_grade(instance)

