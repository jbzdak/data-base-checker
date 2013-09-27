from copy import copy
from django.db import models
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

import bdcheckerapp.autograding

from grading.models._models import PartialGrade, AutogradingResult


class TeamManager(models.Manager):

    def get_team_for_student(self, student, activity):
        try:
            return Team.objects.get(
                Q(student_1=student) | Q(student_2=student), activity=activity
            )
        except Team.DoesNotExist:
            return None

    def get_other_student(self, student, activity):
        team = self.get_team_for_student(student, activity)

        if team is None:
            return None

        if student == team.student_1:
            return team.student_2
        return team.student_1


class Team(models.Model):
    activity = models.ForeignKey("grading.GradeableActivity")
    student_1 = models.ForeignKey("grading.Student")
    student_2 = models.FloatField("grading.Student")

    objects = TeamManager()

def sync_students_in_team(autograding_result):
    partial_grade = autograding_result.partial_grade
    grade_part = partial_grade.grade_part
    sender_student = partial_grade.student
    activity = grade_part.activity

    other = Team.objects.get_other_student(sender_student, activity)

    if other is None:
        return

    grade_copy = copy(autograding_result)
    grade_copy.pk = None
    grade_copy.partial_grade, __ = PartialGrade.objects.get_or_create(
        student = other,
        grade_part = grade_part,
    )
    grade_copy.short_description = "[From team!]:{}".format(autograding_result.short_description)
    grade_copy.save()


@receiver(post_save, sender=AutogradingResult)
def autograding_result_signal(instance, **kwargs):
    if kwargs.get('raw', False):
        return

    sync_students_in_team(instance)
