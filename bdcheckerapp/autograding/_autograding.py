# coding=utf-8
from bdchecker.forms import SQLInputForm

from grading.autograding import Autograder

class SQLAutograder(Autograder):

    @property
    def SubmissionForm(self):
        return SQLInputForm

