# -*- coding: utf-8 -*-
from copy import copy

from threading import local, RLock

from django.db.models.signals import post_save
from django.dispatch import receiver
from bdcheckerapp.models import Team
from grading.models import PartialGrade, AutogradingResult

__local = local()
__local.__dict__.setdefault('executing', False)

def sync_students_in_team_autograding(autograding_result):
    grade_part = autograding_result.grade_part
    sender_student = autograding_result.student
    activity = grade_part.activity

    other = Team.objects.get_other_student(sender_student, activity)

    if other is None:
        return

    grade_copy = copy(autograding_result)
    grade_copy.pk = None
    grade_copy.partial_grade, __ = PartialGrade.objects.get_or_create(
        student = other,
        grade_part = grade_part,
        defaults = {
            "grade" : grade_part.grade
        }
    )
    grade_copy.student = other
    grade_copy.short_description = "[From team!]:{}".format(autograding_result.short_description)
    grade_copy.save()

def sync_students_in_team_partial_grade(partial_grade):
    grade_part = partial_grade.grade_part
    sender_student = partial_grade.student
    activity = grade_part.activity

    other = Team.objects.get_other_student(sender_student, activity)

    if other is None:
        return

    other_grade, __ = PartialGrade.objects.get_or_create(
        student = other,
        grade_part = grade_part,
        defaults = {
            "grade" : partial_grade.grade
        }
    )

    other_grade.grade = partial_grade.grade
    other_grade.short_description = "[From team] {}".format(partial_grade.short_description)
    other_grade.long_description = partial_grade.long_description

    other_grade.save()

# Here is how this shit works:
# 1. One thread can execute only one of these two signals at the time
# 2. Autograding signals kicks in first and suppresses partial_grade signal,
#    which is OK since signals from gradinf will propagate from Autograding change
#    to partial grade change
# 3. If grade is updated manually PartialGrade signal kicks in.


@receiver(post_save, sender=AutogradingResult)
def autograding_result_signal(instance, **kwargs):
    if kwargs.get('raw', False):
        return

    if not getattr(__local, "executing", False):
        try:
            __local.executing = True
            if not getattr(instance, "team_synced", False):
                sync_students_in_team_autograding(instance)
            instance.team_synced = True
        finally:
            __local.executing = False

@receiver(post_save, sender=PartialGrade)
def partial_grade_result_signal(instance, **kwargs):
    if kwargs.get('raw', False):
        return

    if not getattr(__local, "executing", False):
        try:
            __local.executing = True
            sync_students_in_team_partial_grade(instance)
        finally:
            __local.executing = False
