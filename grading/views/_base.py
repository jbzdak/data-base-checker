# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View, TemplateView, ContextMixin
from grading.models._models import Student, AutogradeableGradePart, PartialGrade

__all__ = [
    'StudentView', 'LoginView', 'AutogradeGradePartView', 'GradingBase'
]

class GradingBase(TemplateView):

    template_name = "grading/base.html"

    mixin_template = None

    def get_context_data(self, **kwargs):
        ctx = super(GradingBase, self).get_context_data(**kwargs)
        ctx.update({
            'template_to_include': self.mixin_template
        })
        return ctx


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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, user = self.request.user)
        return super(StudentView, self).dispatch(request, *args, **kwargs)

class AutogradeGradePartView(ContextMixin):
    def __init__(self, **kwargs):
        super(AutogradeGradePartView, self).__init__(**kwargs)
        self.grade_part = None
        self.autograder = None
        self.current_grade = None
        self.student = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['autograder'] = self.autograder
        ctx['grade_part'] = self.grade_part
        ctx['current_grade'] = self.current_grade
        return ctx


    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, user = self.request.user)
        self.grade_part = get_object_or_404(AutogradeableGradePart, pk = kwargs['grade_part'])
        self.autograder = self.grade_part.autograder()

        self.current_grade, __ = PartialGrade.objects.get_or_create(
            grade_part=self.grade_part,
            student=self.student
        )

        return super(AutogradeGradePartView, self).dispatch(request, *args,
                                                            **kwargs)

