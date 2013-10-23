# coding=utf-8

from configparser import ConfigParser
import unittest

from django.utils.translation import ugettext as _
from django.db import transaction, connections, DatabaseError
from django.forms import CharField

from django.forms.models import ModelForm
from django.forms.widgets import Textarea
from bdcheckerapp.utils import make_tc

from grading.autograding import Autograder, GradingResult, AutogradingException
from grading.autograding.autograders.base import ConfigFileBackedAudograder
from grading.models import GradingTextInput


__all__ = ['CompareQueriesAutograder', 'ConfigBackedCompareQueries']

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

    DJANGO_DB = None

    __INVALID_KEYWORDS = [
        'DELETE', 'TRUNCATE', 'DROP', 'CREATE'
    ]

    def __init__(self):
        super(CompareQueriesAutograder, self).__init__()
        self.cf = ConfigParser()
        self.cf.read(self.CONFIG_FILE)

    @property
    def __tc(self):
        return make_tc()

    def __verify_user_sql(self, user_sql):

        for kw in self.__INVALID_KEYWORDS:
            if kw in user_sql:
                message = _("Query contained illegal SQL: {}").format(kw)
                raise AutogradingException(GradingResult(2.0, message))

    def __descr(self, descr):
        return [c[0] for c in descr]

    def __assert_metadata(self, cursor1, cursor2):
        self.__tc.assertEqual(
            self.__descr(cursor1.description),
            self.__descr(cursor2.description),
            _(u"Column metadata is different for model query and your query.")
        )

    def __raise_from_exception(self, exc):
        gr = GradingResult(
            2.0,
            _("There is an syntactic error in your sql code."),
            _("Exception details are: {}").format(str(exc))
        )
        raise AutogradingException(gr) from exc

    def _check_sql(self, sql):
        errors = []
        sql = sql.lower()
        for word in getattr(self, "required_words", []):
            if not word in sql:
                errors.append(_("You did not use word '{}' which is required".format(word)))
        for word in getattr(self, "forbidden_words", []):
            if not word in sql:
                errors.append(_("You did use word '{}' which is forbidden".format(word)))
        subselect_count = getattr(self, "subselect_count", None)
        detected_count = sql.count("select")
        if subselect_count:
            if detected_count <= subselect_count:
                errors.append(_("You must use at least {expected} subselects, I detected you used {used}".format(expected=subselect_count, used=detected_count)))
        if subselect_count == 0:
            if detected_count != 1:
                errors.append(_("You used a subselect which is forbidden".format(subselect_count, detected_count)))


        return errors


    def autograde(self, current_grade, model_instance):

        with transaction.atomic(using=self.DJANGO_DB):

            sql = model_instance.user_input

            self.__verify_user_sql(sql)
            errors = self._check_sql(sql)

            if errors:
                return GradingResult(2.0, "Query is invalid!", errors)

            user_sql = connections[self.DJANGO_DB].cursor()
            expected_sql = connections[self.DJANGO_DB].cursor()

            expected_sql.execute(self.expected_sql)
            try:
                user_sql.execute(sql)
            except DatabaseError as e:
                self.__raise_from_exception(e)

            try:
                if getattr(self, "test_columns", True):
                    self.__assert_metadata(expected_sql, user_sql)

                self.__tc.assertEqual(list(user_sql.fetchall()), list(expected_sql.fetchall()))
            except AssertionError as e:
                return GradingResult(
                    2.0, _("Query returned invalid results"), str(e))

            return GradingResult(5.0, _("OK"))


class ConfigBackedCompareQueries(
    ConfigFileBackedAudograder, CompareQueriesAutograder):

    @property
    def test_columns(self):
        return self.cf.getboolean(self.NAME, "test_columns", fallback=True)

    @property
    def required_words(self):
        words = self.cf.get(self.NAME, "required_words", fallback=None)
        if words is None:
            return []
        return map(lambda x: x.lower(), words.split(","))

    @property
    def forbidden_words(self):
        words = self.cf.get(self.NAME, "forbidden_words", fallback=None)
        if words is None:
            return []
        return map(lambda x: x.lower(), words.split(","))

    @property
    def subselect_count(self):
        return self.cf.getint(self.NAME, "subselect_count", fallback=None)


    @property
    def expected_sql(self):
        return self.cf.get(self.NAME, "sql")
