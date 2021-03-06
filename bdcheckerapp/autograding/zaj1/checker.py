# coding=utf-8
import json

import os

from django.conf import settings

from configparser import ConfigParser
from django import forms
from bdcheckerapp.forms import SQLInputForm
from grading.autograding.autograders import ConfigBackedCompareQueries, CompareFilesAutograder
from grading.autograding.autograders.form_autograder import FormAutograder

DIRNAME = os.path.join(settings.BD_AUTOGRADER_CONFIG_DIR, "zaj1")

CONFIG_FILE = os.path.join(DIRNAME, 'expected_sql.ini')

cp = ConfigParser()
cp.read(CONFIG_FILE)

for section in cp.sections():

    class Zaj1Checker(ConfigBackedCompareQueries):

        NAME = section
        CONFIG_FILE = CONFIG_FILE
        DJANGO_DB = "zaj1db"

        @property
        def SubmissionForm(self):
            return SQLInputForm

class Zaj1Task1(CompareFilesAutograder):

    NAME = "zaj1task1"
    DESCRIPTION = "Zadanie 1: Załącz plik wygenerowany przez polecienie psql"
    EXPECTED_FILE = os.path.join(DIRNAME, "zad1_out.csv")

class Zaj1Task2(CompareFilesAutograder):

    NAME = "zaj1task2"
    DESCRIPTION = "Zadanie 2: Załącz plik wygenerowany przez polecienie psql"
    EXPECTED_FILE = os.path.join(DIRNAME, "task2.csv")

class Zaj1Task8(FormAutograder):

    class QuestionForm(forms.Form):
        __lbl = "Średnia prędkość wiatru dla dni w których przekroczony został poziom pyłu zawieszonego PM10"
        exceeded_wind_speed = forms.CharField(label=__lbl)
        __lbl = "Średnia prędkość wiatru dla dni w których nie został przekroczony został poziom pyłu zawieszonego PM10"
        not_exceeded_wind_speed = forms.CharField(label=__lbl)

        def clean_exceeded_wind_speed(self):
            return self.cleaned_data.get("exceeded_wind_speed", "").replace(",", ".")

        def clean_not_exceeded_wind_speed(self):
            return self.cleaned_data.get("not_exceeded_wind_speed", "").replace(",", ".")

    INTERNAL_FORM = QuestionForm

    NAME="zaj1task8"
    DESCRIPTION = "Zadanie 8: Podaj średnie prędkości wiatru dla danych spełniających kryteria"

    with open(os.path.join(DIRNAME, "task8expeted.json")) as f:
        EXPECTED_DATA = json.load(f)

class Zaj1Task11(FormAutograder):

    class QuestionForm(forms.Form):
        max_avg = forms.CharField(label="Proszę wybrać miesiąc z najwyżym średnim poziomem pm_10, z dokładnością do 0.01")

        def clean_max_avg(self):
            return self.cleaned_data.get("max_avg", "").replace(",", ".")

    INTERNAL_FORM = QuestionForm

    NAME="zaj1task11"
    with open(os.path.join(DIRNAME, "task11expected.json")) as f:
        EXPECTED_DATA = json.load(f)


class Zaj1Task12(FormAutograder):

    class QuestionForm(forms.Form):
        days = forms.CharField(label="Proszę wybrać ilość dni ze średnim poziomem pm_10 przekraczającym dopuszczalny poziom wynoszący 50 (mikrogramów na metr sześcienny). 1")

        def clean_days(self):
            return self.cleaned_data.get("days", "").replace(",", ".")

    INTERNAL_FORM = QuestionForm

    NAME="zaj1task12"
    DESCRIPTION = "Zadanie 12: Podaj średnie prędkości wiatru dla danych spełniających kryteria"

    with open(os.path.join(DIRNAME, "task12expected.json")) as f:
        EXPECTED_DATA = json.load(f)