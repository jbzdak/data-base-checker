# -*- coding: utf-8 -*-
from django import forms

class TestForm(forms.Form):

    input = forms.IntegerField("Input 2")