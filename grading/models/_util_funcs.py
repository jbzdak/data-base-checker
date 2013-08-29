# coding=utf-8
from grading.models._models import StudentGrade, GradePart, PartialGrade

__all__ = ['sync_grade', 'sync_grades_for_activity', 'sync_grades_for_student']

def sync_grades_for_activity(activity):
    for group in activity.groups.all():
        for student in group.students.all():
            StudentGrade.objects.get_or_create(
                student = student,
                activity = activity,
                defaults = {
                    "grade": 0.0
                }
            )

def sync_grades_for_student(student):
    for activity in student.group.activities.all():
        StudentGrade.objects.get_or_create(
                student = student,
                activity = activity,
                defaults = {
                    "grade": 0.0
                }
        )

def calculate_grade(grades, weights = None):
    if weights is None:
        weights = [1 for g in grades]

    if not len(grades) == len(weights):
        raise ValueError("Length of partial grades array and weights must be equal")

    weighted = [g*w for g, w in zip(grades,weights)]

    grade = sum(weighted)/sum(weights)

    return grade

def grade_student(activity, student):
    grade_parts = GradePart.objects.filter(
        activity = activity
    )
    grades = []
    weights = []

    for gp in grade_parts.all():
        weights.append(gp.weight)
        try:
            partial_grade = PartialGrade.objects.get(
                grade__activity = activity,
                student = student
            )
        except GradePart.DoesNotExist:
            grades.append(gp.default_grade)
        else:
            grades.append(partial_grade.grade)

    return calculate_grade(grades, weights)

def sync_grade(grade):
    activity = grade.activity
    student = grade.student

    grade = grade_student(activity, student)

    grade_model, created = StudentGrade.objects.get_or_create(
        student = student,
        activity = activity,
        defaults = {
            "grade": 0.0
        }
    )
    grade_model.grade = grade
    grade_model.save()
