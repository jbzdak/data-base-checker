# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from grading.views._base import *

from grading.models import *


class GradeTask(AutogradeGradePartView, FormView):

    template_name = "grading/display_form.html"


    def get_form_class(self):
        return self.autograder.SubmissionForm

    def form_valid(self, form):

        instance = form.save()

        resut = self.autograder.autograde(self.current_grade, instance)
        autograding_result_model, __ = AutogradingResult.objects.get_or_create(
            student = self.student,
            grade_part = self.grade_part,
            defaults = {
                'grade': self.grade_part.default_grade
            }
        )
        autograding_result_model.fill(instance, resut)
        autograding_result_model.save()

        return redirect("show-result", pk=autograding_result_model.pk)

class GradingResult(StudentView, TemplateView):

    template_name = "grading/base.html"

    def dispatch(self, request, *args, **kwargs):
        self.autograde_result = AutogradingResult.objects.get(pk = kwargs['pk'])
        result = super(GradingResult, self).dispatch(request, *args, **kwargs)
        if self.autograde_result.student != self.student:
            return HttpResponse(status=403)
        return result

    def get_context_data(self, **kwargs):
        ctx =  super(GradingResult, self).get_context_data(**kwargs)
        ctx['object'] = self.autograde_result
        ctx['template_to_include'] = 'grading/autograde_result.html'
        return ctx

class CourseView(StudentView, GradingBase):

    mixin_template = "grading/course.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.course =  get_object_or_404(Course, slug_field=kwargs['name'])
        return super(CourseView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        ctx = super(CourseView, self).get_context_data(**kwargs)
        ctx.update({
            'course': self.course
        })
        return ctx


class GradeActivity(StudentView, GradingBase):

    mixin_template = 'autograding/autograde_activity.html'

    def dispatch(self, request, *args, **kwargs):
        self.activity = get_object_or_404(GradeableActivity, slug_field=kwargs['name'])
        return super(GradeActivity, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        ctx =  super(GradeActivity, self).get_context_data(**kwargs)
        ctx.update({
            "student": self.student,
            "activity": self.activity
        })
        return ctx


