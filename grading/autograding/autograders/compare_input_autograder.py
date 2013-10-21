# -*- coding: utf-8 -*-
import unittest
from bdcheckerapp.utils import make_tc
from grading.autograding import Autograder
from django import forms
from django.utils.translation import ugettext_lazy as _
from grading.autograding._base import AutogradingException, GradingResult
from grading.models import GradingTextInput

__all__ = ["CompareFilesAutograder"]

class CompareFileForm(forms.Form):

    MAX_FILE_SIZE=None

    submitted_file = forms.FileField(_("Submitted file"))

    def clean(self):
        if not self.errors:
            return {
                "user_input": str(self.cleaned_data['submitted_file'].read(), encoding="utf-8")
            }
        return {}


    def save(self, commit=True, **kwargs):

        model = GradingTextInput()
        model.user_input = self.cleaned_data['user_input']

        if commit:
            model.save()

        return model


class CompareFilesAutograder(Autograder):

    MAX_FILE_SIZE = 1024*1024

    EXPECTED_FILE = None

    @property
    def __tc(self):
        return make_tc()

    @property
    def SubmissionModel(self):
        return GradingTextInput

    @property
    def SubmissionForm(self):
        class TmpForm(CompareFileForm):
            MAX_FILE_SIZE = self.MAX_FILE_SIZE

        return TmpForm


    def compare_file_contents(self, expected, user_input):
        try:
            self.__tc.assertEqual(expected, user_input)
        except AssertionError as e:
            raise AutogradingException(
                GradingResult(
                    2.0,
                    _("File contents are different than expected"),
                    self.__LONG_ERROR_MESSAGE_PATTERN.format(diff=e.args[0])
                )
            ) from e
        return GradingResult(5.0, "OK")

    def autograde(self, current_grade, model_instance):

        with open(self.EXPECTED_FILE) as f:
            expected_contents = f.read()

        user_contents = model_instance.user_input

        return self.compare_file_contents(expected_contents, user_contents)

    __FILE_TO_BIG_MSG =_("File is to large to be graded, this submission allows maximum of {max_size} bytes")

    __LONG_ERROR_MESSAGE_PATTERN = _("Content comparator returned following diff\n: {diff}")






