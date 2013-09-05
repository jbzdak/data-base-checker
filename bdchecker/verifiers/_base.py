# coding=utf-8
import abc
from copy import copy

__VERIFIER_CACHE = {}

def get_verifiers():
    """
    >>> @verifier("foo")
    ... class Test(Verifier):
    ...     pass
    >>> __VERIFIER_CACHE['foo']
    <class '_base.Test'>

    >>> get_verifiers() == __VERIFIER_CACHE
    True
    >>> get_verifiers() is __VERIFIER_CACHE
    False
    """
    return copy(__VERIFIER_CACHE)


def verifier(name):
    """

    >>> @verifier("foo")
    ... class Test(Verifier):
    ...     pass
    >>> __VERIFIER_CACHE['foo']
    <class '_base.Test'>

    >>> @verifier("foo")
    ... class Bar(object):
    ...     pass
    Traceback (most recent call last):
    ValueError
    """
    def decorator(decorated_type):
        if not issubclass(decorated_type, Verifier):
            raise ValueError()
        __VERIFIER_CACHE[name] = decorated_type
        return type
    return decorator

class VerifyResult(object):

    def __init__(self):
        self.grade = None
        self.message = None

    def as_dict(self):
        return {
            "grade": self.grade,
            "message": self.message
        }

class VerifierInput(object):

    def __init__(self):
        self.input_string = None

class Verifier(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, verifier_input):
        """
        :returns: verification results
        :rtype:VerifyResult
        """



