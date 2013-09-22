# coding=utf-8

from django import template
from grading.models import GradePart, PartialGrade, AutogradeableGradePart

register = template.Library()

@register.filter
def grade_for_student(grade_part, student):
    try:
        return PartialGrade.objects.get(
            grade_part=grade_part,
            student = student
        )
    except PartialGrade.DoesNotExist:
        return None


@register.filter
def can_grade(grade_part, student):
    if not isinstance(grade_part, AutogradeableGradePart):
        try:
            grade_part = AutogradeableGradePart.objects.get(
                parent = grade_part
            )
        except AutogradeableGradePart.DoesNotExist:
            return False
    return grade_part.autograder().can_grade_student(student)