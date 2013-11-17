# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from grading.autograding import AutogradingException
from grading.autograding._base import OfflineAutograder

from grading.views._base import *

from grading.models import *


class GradeTask(AutogradeGradePartView, FormView):

    template_name = "autograding/do_autograding.html"

    def get_form_class(self):
        return self.autograder.SubmissionForm

    def form_valid(self, form):

        instance = form.save()

        if not self.autograder.can_grade_student(self.grade_part, self.student):
            raise PermissionDenied()


        autograding_result_model = AutogradingResult(
            student = self.student,
            grade_part = self.grade_part,
        )
        autograding_result_model.fill_empty(instance)
        autograding_result_model.save()

        if isinstance(self.autograder, OfflineAutograder) and settings.ALLOW_OFFILNE_GRADING:
            self.autograder.autograde_offline(
                self.current_grade,
                instance,
                autograding_result_model
            )
        else:
            try:
                resut = self.autograder.autograde(self.current_grade, instance)
            except AutogradingException as e:
                resut = e.grading_result
            autograding_result_model.fill(instance, resut)
            autograding_result_model.save()

        return redirect("show-result", pk=autograding_result_model.pk)

class GradingResult(StudentView, GradingBase):

    template_name = "autograding/autograde_result.html"


    def dispatch(self, request, *args, **kwargs):
        self.autograde_result = AutogradingResult.objects.get(pk = kwargs['pk'])
        result = super(GradingResult, self).dispatch(request, *args, **kwargs)
        if self.autograde_result.student != self.student:
            return HttpResponse(status=403)
        return result

    def get_context_data(self, **kwargs):
        ctx = super(GradingResult, self).get_context_data(**kwargs)
        ctx['object'] = self.autograde_result
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
            "activity": self.activity,
            "student_grade": get_object_or_404(StudentGrade, student=self.student, activity=self.activity)
        })
        return ctx


