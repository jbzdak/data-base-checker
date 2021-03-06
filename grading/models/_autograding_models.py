# coding=utf-8
from django.core.exceptions import ValidationError

from django.db import models

__all__ = ['GradingBooleanInput', 'GradingTextInput']

class GradingBooleanInput(models.Model):

    user_input = models.BooleanField(default=False)

    required_input = models.BooleanField(blank=False, default=False)

    def clean(self):
        if not self.required_input:
            raise ValidationError("Fill required input")

    class Meta:
        app_label = "grading"

class GradingTextInput(models.Model):

    user_input = models.TextField(blank=False)

    class Meta:
        app_label = "grading"