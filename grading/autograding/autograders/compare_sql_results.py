# coding=utf-8

from configparser import ConfigParser
import unittest
from django.db import transaction, connection
from django.forms import CharField

from django.forms.models import ModelForm
from django.forms.widgets import Textarea

from grading.autograding import Autograder, GradingResult, AutogradingException
from grading.models import GradingTextInput


class SQLInputForm(ModelForm):

    user_input = CharField(
        widget=Textarea()
    )

    class Meta:
        model = GradingTextInput



class SQLAutograder(Autograder):

    @property
    def SubmissionForm(self):
        return SQLInputForm


class CompareQueriesAutograder(SQLAutograder):

    CONFIG_FILE = None

    DJANGO_DB = None

    __INVALID_KEYWORDS = [
        'DELETE', 'TRUNCATE', 'DROP', 'CREATE'
    ]

    def __init__(self):
        super(CompareQueriesAutograder, self).__init__()
        self.cf = ConfigParser()
        self.cf.read(self.CONFIG_FILE)

    @property
    def expected_sql(self):
        return self.cf.get('DEFAULT', self.NAME)

    @property
    def __tc(self):
        tc = unittest.TestCase()
        tc.longMessage = True
        tc.maxDiff = 2000
        return tc

    def __verify_user_sql(self, user_sql):

        for kw in self.__INVALID_KEYWORDS:
            if kw in user_sql:
                message = "Zapytanie zawierało niedozwolone słowo kluczowe SQL: {}".format(kw)
                raise AutogradingException(GradingResult(2.0, message))




    def __descr(self, descr):
        return [c[0] for c in descr]

    def __assert_metadata(self, cursor1, cursor2):
        self.__tc.assertEqual(
            self.__descr(cursor1.description),
            self.__descr(cursor2.description),
            u"Opisy kolumn są różne dla Waszego zapytania oraz zapytania modelowego. " +
            u"Sprawdź proszę kolumny zapytań."
        )


    def autograde(self, current_grade, model_instance):

        with transaction.atomic(using=self.DJANGO_DB):

            sql = model_instance.user_input

            self.__verify_user_sql(sql)

            user_sql = connection[self.DJANGO_DB].cursor()
            expected_sql = connection[self.DJANGO_DB].cursor()

            expected_sql.execute(self.expected_sql)
            user_sql.execute(sql)

            try:
                self.__assert_metadata(expected_sql, user_sql)
                self.__tc.assertEqual(list(user_sql.fetchall()), list(expected_sql.fetchall()))
            except AssertionError as e:
                return GradingResult(
                    2.0, "Niepoprawny wynik zapytania", e.message)

            return GradingResult(5.0, "Wszystko działa")


