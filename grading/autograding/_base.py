# coding=utf-8
import abc
from copy import copy
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import six

__all__ = [
    'get_autograders', 'GradingResult', 'AutogradingException', 'Autograder',
    'OfflineAutograder'
]

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

class BaseAutograder(six.with_metaclass(AutograderMetaclass)):

    NAME = None

    DESCRIPTION = None

    # TODO: Add question randomisation

    # TODO: Convert parameters from most methods to __init__ args so we can
    # customize behavioiu in all megtods

    @property
    @abc.abstractmethod
    def SubmissionForm(self):
        raise ValueError

    @property
    def description(self):
        return self.DESCRIPTION

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

    @property
    def redirect(self, autograding_result):
        return reverse("show-result", pk=autograding_result.pk)


class Autograder(BaseAutograder):

    """
    Subclasses of this class encapsulate autograding process in cases when
    autograding process is performed on-line (is fast and can be peformed
    during request processing)
    """

    @abc.abstractmethod
    def autograde(self, current_grade, model_instance):
        """
        :param current_grade: Current grade for this activity part,
        :type current_grade: :class:`.GradePart`
        :param model_instance: User sumbission
        :type: :attr:`SubmissionModel`

        :returns: verification results
        :rtype:VerifyResult

        :raises:`AutogradingException` This exception is alternate way to return
        grade it typically means thtah student input was invalid
        """

class OfflineAutograder(Autograder):

    """
    Subclasses of this class encapsulate autograding process when autograding
    can take long time.
    """

    @abc.abstractmethod
    def autograde_offline(self, current_grade, model_instance, grading_result_model):
        """
        This method takes similar parameters to :meth:`.Autograder.autograde`,

        This instance should  initiate grading process and then exit.

        To store intermediate grading results you might update:
        ``grading_result_model.grading_result`` (and then save this model).

        To finish grading set `grading_result_model.is_pending`` to true
        (and then save this model).

        :param current_grade: Current grade for this activity part,
        :type current_grade: :class:`.GradePart`
        :param model_instance: User sumbission
        :type: :attr:`SubmissionModel`
        :param grading_result_model: Model that should be used to store
          grading result, when grading process is finished.
        :type: :class:`.AutogradingResult`

        """




