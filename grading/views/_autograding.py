# coding=utf-8
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
        autograding_result_model = AutogradingResult()
        autograding_result_model.fill(instance, resut)
        autograding_result_model.save()

        return super(GradeTask, self).form_valid(form)

