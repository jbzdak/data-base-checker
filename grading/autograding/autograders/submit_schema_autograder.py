# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from grading.models import GradingTextInput



class CompareFileForm(forms.Form):

    MAX_FILE_SIZE=None

    submitted_text = forms.CharField(label=_("Submitted schema"), widget=forms.Textarea, required=False)
    submitted_file = forms.FileField(label=_("Submitted schema file"), required=False)

    def clean(self):

        if not (self.cleaned_data.get('submitted_text', None) or  self.cleaned_data.get('submitted_file', None)):
            raise ValidationError(_("Please submit either schema text or schema file"))

        if self.cleaned_data.get('submitted_text', None) and self.cleaned_data.get('submitted_file', None):
            raise ValidationError(_("Please submit either schema text or schema file, and not both"))

        if self.cleaned_data.get('submitted_file', None):
            user_input =  str(self.cleaned_data['submitted_file'].read(), encoding="utf-8")
        else:
            user_input = self.cleaned_data['submitted_text']

        if not self.errors:
            return {
                "user_input": user_input
            }
        return {}


    def save(self, commit=True, **kwargs):

        model = GradingTextInput()
        model.user_input = self.cleaned_data['user_input']

        if commit:
            model.save()

        return model
