# coding=utf-8

from django.db import models

class GradingBooleanInput(models.Model):

    user_input = models.BooleanField(default=False)

    class Meta:
        app_label = "grading"