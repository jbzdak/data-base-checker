# -*- coding: utf-8 -*-
import json
from django.forms.forms import Form
from grading.autograding import Autograder
from grading.autograding._base import GradingResult
from grading.models._autograding_models import GradingTextInput
from django.utils.translation import ugettext_lazy as _


class FormAutograder(Autograder):

    INTERNAL_FORM = None

    EXPECTED_DATA = None


    @property
    def SubmissionModel(self):
        return GradingTextInput

    @property
    def SubmissionForm(self):

        class WrapperForm(self.INTERNAL_FORM):

            def save(self, commit=True, **kwargs):
                submitted_data = self.cleaned_data
                model = GradingTextInput()
                model.user_input = json.dumps(submitted_data)
                if commit:
                    model.save()
                return model

        return WrapperForm

    def autograde(self, current_grade, model_instance):
        submitted_data = json.loads(model_instance.user_input)

        error_fields = []

        for k, v in self.EXPECTED_DATA.items():
            if v != submitted_data.get(k, object()):
                error_fields.append(k)

        if not error_fields:
            return GradingResult(5.0, "OK")

        field_form_map = {f.name:f.label for f in self.SubmissionForm()}
        error_labels = []

        for field in error_fields:
            error_labels.append(field_form_map[field])

        return GradingResult(2.0, self.__INVALID_ENTRIES.format(error_labels))

    __INVALID_ENTRIES = _("Following entries were invalid: {}")





