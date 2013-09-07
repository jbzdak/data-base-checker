# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from grading.models._models import Student, AutogradeableGradePart, PartialGrade

__all__ = ['StudentView', 'LoginView', 'AutogradeGradePartView']

class LoginView(View):

    def __init__(self, **kwargs):
        self.request = None
        super(LoginView, self).__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)


class StudentView(LoginView):

    def __init__(self, **kwargs):
        super(StudentView, self).__init__(**kwargs)
        self.student = None

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, user = self.request.user)
        return super(StudentView, self).dispatch(request, *args, **kwargs)

class AutogradeGradePartView(StudentView):
    def __init__(self, **kwargs):
        super(AutogradeGradePartView, self).__init__(**kwargs)
        self.grade_part = None
        self.autograder = None
        self.current_grade = None

    def dispatch(self, request, *args, **kwargs):
        self.grade_part = get_object_or_404(AutogradeableGradePart, pk = kwargs['grade_part'])
        self.autograder = self.grade_part.autograder()
        try:
            self.current_grade = PartialGrade.objects.get(
                grade_part=self.grade_part,
                student=self.student
            )
        except PartialGrade.DoesNotExist:
            pass
        return super(AutogradeGradePartView, self).dispatch(request, *args,
                                                            **kwargs)

