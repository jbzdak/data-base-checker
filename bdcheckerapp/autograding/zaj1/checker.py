# coding=utf-8

import os
from configparser import ConfigParser
from bdcheckerapp.forms import SQLInputForm
from grading.autograding.autograders.compare_sql_results import CompareQueriesAutograder

DIRNAME = os.path.abspath(os.path.split(__file__)[0])

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
