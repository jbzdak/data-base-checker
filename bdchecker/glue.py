# -*- coding: utf-8 -*-
from django.utils.translation import ugettext
from bdcheckerapp.forms import SchemaInputForm
from grading.autograding._base import GradingResult
from grading.autograding.celery.autograders import CeleryAutograder
from grading.models import GradingTextInput


class BaseTaskCheckerAutograder(CeleryAutograder):

    TaskChecker = None

    @property
    def SubmissionForm(self):
        return SchemaInputForm

    @property
    def SubmissionModel(self):
        return GradingTextInput

    def autograde(self, current_grade, model_instance):
        tc = self.TaskChecker(schema=model_instance.user_input)
        passed, mark, long_description = tc.perform_grading()
        grade = mark/2
        if passed:
            short_description = ugettext("OK")
        else:
            short_description = ugettext("Failed, see details")
        return GradingResult(
            grade,
            short_description,
            long_description
        )
