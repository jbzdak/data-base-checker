# coding=utf-8
from django.forms.fields import CharField
from django.forms.models import ModelForm
from django.forms.widgets import Textarea
from grading.models import GradingTextInput


class SQLInputForm(ModelForm):

    user_input = CharField(
        widget=Textarea()
    )

    class Meta:
        model = GradingTextInput

    class Media:

        __js_pref = 'codemirror/js/'
        __css_pref = 'codemirror/css/'

        css = [
            __css_pref + 'codemirror.css',
            __css_pref + 'sql.css']
        js = [
            __js_pref + '/codemirror.js',
            __js_pref + '/base16-light.css',
            'bdhecker/load_codemirror.js'
        ]