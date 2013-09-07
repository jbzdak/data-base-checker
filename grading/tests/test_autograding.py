# coding=utf-8
from django.test.testcases import TestCase
from grading.autograding import *

class TestAutograderMetaclass(TestCase):

    def test_metaclass(self):
        grader_name = "test123"
        self.assertNotIn(grader_name, get_autograders().keys())
        class TestAutohrader(Autograder):

            NAME = grader_name

            @property
            def SubmissionForm(self):
                pass

            def autograde(self, model_instance):
                pass

        self.assertIn(grader_name, get_autograders().keys())
        self.assertIs(get_autograders()[grader_name], TestAutohrader)