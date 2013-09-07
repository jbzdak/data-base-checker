# coding=utf-8
from django.db import models
from django.forms.models import ModelForm
from grading.autograding import Autograder
from grading.autograding._base import GradingResult

"""

"""

class BooleanInput(models.Model):

    user_input = models.BooleanField(default=False)

class BooleanForm(ModelForm):

    class Meta:
        model = BooleanInput

class TestAutoGrader(Autograder):

    NAME = "test"

    def SubmissionForm(self):
        return BooleanForm

    def autograde(self, current_grade, model_instance):
        if model_instance.user_input:
            return GradingResult(
                grade=5.0,
                comment = "OK")
        return GradingResult(
            grade=2.0,
            comment="Zaznacz to pole :P"
        )

