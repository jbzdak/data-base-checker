# coding=utf-8
from grading.models._models import StudentGrade, GradePart, PartialGrade

__all__ = [
    'sync_partial_grade', 'sync_grades_for_activity',
    'sync_grades_for_student', 'grade_student', 'calculate_grade',
    'sync_partial_grade_with_autograde'
]

def sync_grades_for_activity(activity):
    for group in activity.courses.all():
        for student in group.students.all():
            sync_grade(activity, student)

def sync_grades_for_student(student):
    for activity in student.course.activities.all():
        sync_grade(activity, student)

def calculate_grade(grades, weights = None):
    if weights is None:
        weights = [1 for g in grades]

    weights = [float(w) for w in weights]
    grades = [float(g) for g in grades]

    if not len(grades) == len(weights):
        raise ValueError("Length of partial grades array and weights must be equal")

    weighted = [g*w for g, w in zip(grades,weights)]

    grade = sum(weighted)/float(sum(weights))

    return grade

def grade_student(activity, student):
    grade_parts = GradePart.objects.filter(
        activity = activity
    )
    grades = []
    weights = []

    required_grade_missing = False

    if len(grade_parts.all()) == 0:
        return activity.default_grade

    for gp in grade_parts.all():
        weights.append(gp.weight)
        try:
            partial_grade = PartialGrade.objects.get(
                grade_part = gp,
                student = student
            )
            if gp.required and gp.passing_grade is not None:
                if partial_grade.grade < gp.passing_grade:
                    required_grade_missing = True

        except PartialGrade.DoesNotExist:
            grades.append(gp.default_grade)
            if gp.required:
                required_grade_missing = True
        else:
            grades.append(partial_grade.grade)

    if required_grade_missing:
        return activity.default_grade

    return calculate_grade(grades, weights)

def sync_grade(activity, student):
    grade_model, created = StudentGrade.objects.get_or_create(
        student = student,
        activity = activity,
        defaults = {
            "grade": 0.0
        }
    )
    grade = grade_student(activity, student)
    grade_model.grade = grade
    grade_model.save()

def sync_partial_grade(grade):
    activity = grade.grade_part.activity
    student = grade.student

    sync_grade(activity, student)

def sync_partial_grade_with_autograde(autograde):

    currently_syncing = getattr(autograde, "currently_syncing", False)

    if not currently_syncing:

        autograde.currently_syncing = True

        try:

            partial_grade, __ = PartialGrade.objects.get_or_create(
                student = autograde.student,
                grade_part = autograde.grade_part,
                defaults = {
                    "grade" : autograde.grade
                }
            )
            partial_grade.short_description = autograde.short_description
            partial_grade.long_description = autograde.long_description
            partial_grade.grade = autograde.grade
            partial_grade.save()

            autograde.already_synced = True

            autograde.partial_grade = partial_grade
            autograde.save()
        finally:
            autograde.currently_syncing = False