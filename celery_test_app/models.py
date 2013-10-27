from django.db import models

# Create your models here.
from django.forms.models import ModelForm
from grading.autograding import OfflineAutograder
from grading.autograding._base import GradingResult
from grading.autograding.celery.autograders import CeleryAutograder
from grading.models import GradingBooleanInput


class InputAutograder(CeleryAutograder):

    NAME = "TestCeleryAutograder"

    @property
    def SubmissionForm(self):
        class XXX(ModelForm):
            class Meta:
                model = GradingBooleanInput

        return XXX


    def autograde(self, current_grade, model_instance):
        if model_instance.user_input:
            return GradingResult(5, 'OK')
        return GradingResult(2.0, "zaznacz to pole tekstowe")