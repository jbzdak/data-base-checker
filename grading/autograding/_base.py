# coding=utf-8
import abc
from copy import copy
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils import six

_AUTOGRADER_CACHE = {}

def get_autograders():
    """

    >>> _AUTOGRADER_CACHE

    >>> class Test(Autograder):
    ...     pass
    >>> _AUTOGRADER_CACHE['foo']
    <class '_base.Test'>

    >>> get_autograders() == _AUTOGRADER_CACHE
    True
    >>> get_autograders() is _AUTOGRADER_CACHE
    False
    """
    return copy(_AUTOGRADER_CACHE)


class AutograderMetaclass(abc.ABCMeta):
    def __new__(cls, *args, **kwargs):
        type = super(AutograderMetaclass, cls).__new__(cls, *args, **kwargs)
        cls.__maybe_add(type)
        return type

    @staticmethod
    def __maybe_add(type):
        if getattr(type, "__abstractmethods__", set()):
            return
        if not getattr(type, "NAME", None):
            return
        if not isinstance(type.NAME, six.text_type):
            raise ValueError("Autograder name {} is not an instance of {}".format(type.NAME, six.text_type))
        _AUTOGRADER_CACHE[type.NAME] = type


class AutogradingException(Exception):

    def __init__(self, grading_result):
        super(AutogradingException, self).__init__()
        self.grading_result = grading_result


class GradingResult(object):

    template_name = "autograding/grading_result_default_template.html"

    def __init__(self, grade, comment, long_message=None):
        super(GradingResult, self).__init__()
        self.grade = grade
        self.comment = comment
        self.long_message = long_message

    def get_template_name(self):
        return self.template_name

    def grading_ctx(self):
        return {
            "obj": self
        }

    def render(self):
        return render_to_string(self.get_template_name(), self.grading_ctx())

class Autograder(six.with_metaclass(AutograderMetaclass)):


    NAME = None

    DESCRIPTION = None

    # TODO: Add question randomisation

    @property
    @abc.abstractmethod
    def SubmissionForm(self):
        raise ValueError

    @property
    def SubmissionModel(self):
        return self.SubmissionForm._meta.model

    @property
    def submission_contenttype(self):
        return ContentType.objects.get_for_model(self.SubmissionModel)

    def can_grade_student(self, grade_part, student):
        if grade_part.may_be_autograded_to is None:
            return True
        return datetime.now() < grade_part.may_be_autograded_to

    @abc.abstractmethod
    def autograde(self, current_grade, model_instance):
        """
        :returns: verification results
        :rtype:VerifyResult

        :raises:`AutogradingException` This exception is alternate way to return
        grade it typically means thtah student input was invalid
        """
