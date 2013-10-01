# coding=utf-8
from datetime import datetime, timedelta
from django.test.testcases import TestCase
from grading.autograding import *
from grading.models import AutogradeableGradePart


class TestAutograderMetaclass(TestCase):

    def test_metaclass_positive(self):
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

    def test_metaclass_no_name(self):
        class TestAutohrader(Autograder):
            @property
            def SubmissionForm(self):
                pass

            def autograde(self, model_instance):
                pass

        self.assertNotIn(TestAutohrader, get_autograders().values())

class TestCanAutograde(TestCase):

    def setUp(self):
        self.grade_part = AutogradeableGradePart()
        self.autograder = get_autograders()['test']()

    def test_default_may_autograde(self):
        self.assertTrue(self.autograder.can_grade_student(self.grade_part, None))

    def test_can_autograde_before_expiry_autograde(self):
        self.grade_part.may_be_autograded_to = datetime.now() + timedelta(minutes=1)
        self.assertTrue(self.autograder.can_grade_student(self.grade_part, None))

    def test_can_autograde_before_after_autograde(self):
        self.grade_part.may_be_autograded_to = datetime.now() - timedelta(minutes=1)
        self.assertFalse(self.autograder.can_grade_student(self.grade_part, None))