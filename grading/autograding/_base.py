# coding=utf-8
import abc
from copy import copy
from django.contrib.contenttypes.models import ContentType

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
        if not getattr(type, "__abstractmethods__", set()):
            _AUTOGRADER_CACHE[type.NAME] = type
        return type

class GradingResult(object):
    def __init__(self, grade, comment):
        super(GradingResult, self).__init__()
        self.grade = grade
        self.comment = comment

    def render(self):
        #TODO do it better
        return """
        Grade {}
        """.format(self.grade)


class Autograder(object):

    __metaclass__ = AutograderMetaclass

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

    @abc.abstractmethod
    def autograde(self, current_grade, model_instance):
        """
        :returns: verification results
        :rtype:VerifyResult
        """
