# coding=utf-8
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from grading.models import GradingTextInput

from registration.forms import RegistrationForm


class BDRegistrationForm(RegistrationForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    email = forms.EmailField(label=_("E-mail"))


    #first_name = forms.CharField(label="Imię")
    #last_name = forms.CharField(label="Nazwisko")
    student_id = forms.CharField(label="Numer indeksu")


    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))


class SQLInputForm(ModelForm):

    user_input = forms.CharField(
        widget=forms.Textarea(), label="Wprowadź swoje zapytanie"
    )

    class Meta:
        model = GradingTextInput

    class Media:

        __js_pref = 'codemirror/js/'
        __css_pref = 'codemirror/css/'

        css = {
            "all": [
                __css_pref + 'codemirror.css',
                __css_pref + 'base16-dark.css'
            ]
        }
        js = [
            __js_pref + '/codemirror.js',
            __js_pref + '/sql.js',
            'bdhecker/load_codemirror.js'
        ]