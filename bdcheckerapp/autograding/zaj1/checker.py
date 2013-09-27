# coding=utf-8
import json

import os

from django.conf import settings

from configparser import ConfigParser
from django import forms
from bdcheckerapp.forms import SQLInputForm
from grading.autograding.autograders import CompareQueriesAutograder, CompareFilesAutograder
from grading.autograding.autograders.form_autograder import FormAutograder

DIRNAME = os.path.join(settings.BD_AUTOGRADER_CONFIG_DIR, "zaj1")

CONFIG_FILE = os.path.join(DIRNAME, 'expected_sql.ini')

cp = ConfigParser()
cp.read(CONFIG_FILE)

for key in cp['DEFAULT']:
    if key.endswith('description'):
        continue

    class Zaj1Checker(CompareQueriesAutograder):

        NAME = key
        CONFIG_FILE = CONFIG_FILE
        DESCRIPTION = cp.get('DEFAULT', key + '.description', fallback=None)
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

    INTERNAL_FORM = QuestionForm

    NAME="zaj1task8"
    DESCRIPTION = "Zadanie 8: Podaj średnie prędkości wiatru dla danych spełniających kryteria"

    with open(os.path.join(DIRNAME, "task8expeted.json")) as f:
        EXPECTED_DATA = json.load(f)

class Zaj1Task11(FormAutograder):

    class QuestionForm(forms.Form):
        max_avg = forms.CharField(label="Proszę wybrać miesiąc z najwyżym średnim poziomem pm_10, z dokładnością do 0.01")

    INTERNAL_FORM = QuestionForm

    NAME="zaj1task11"
    with open(os.path.join(DIRNAME, "task11expected.json")) as f:
        EXPECTED_DATA = json.load(f)


class Zaj1Task12(FormAutograder):

    class QuestionForm(forms.Form):
        days = forms.CharField(label="Proszę wybrać ilość dni ze średnim poziomem pm_10 przekraczającym dopuszczalny poziom wynoszący 50 (mikrogramów na metr sześcienny). 1")

    INTERNAL_FORM = QuestionForm

    NAME="zaj1task12"
    DESCRIPTION = "Zadanie 8: Podaj średnie prędkości wiatru dla danych spełniających kryteria"

    with open(os.path.join(DIRNAME, "task11expected.json")) as f:
        EXPECTED_DATA = json.load(f)