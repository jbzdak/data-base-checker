# coding=utf-8
import json

import os

from django.conf import settings

from configparser import ConfigParser
from django import forms
from bdcheckerapp.forms import SQLInputForm
from grading.autograding.autograders import CompareQueriesAutograder, CompareFilesAutograder, ConfigBackedCompareQueries
from grading.autograding.autograders.form_autograder import FormAutograder

DIRNAME = os.path.join(settings.BD_AUTOGRADER_CONFIG_DIR, "zaj2")

CONFIG_FILE = os.path.join(DIRNAME, 'expected_sql.ini')

cp = ConfigParser()
cp.read(CONFIG_FILE)


for section in cp.sections():

    class Zaj1Checker(ConfigBackedCompareQueries):

        NAME = section
        CONFIG_FILE = CONFIG_FILE
        DJANGO_DB = "za21db"

        @property
        def SubmissionForm(self):
            return SQLInputForm
