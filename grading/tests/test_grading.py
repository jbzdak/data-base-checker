# coding=utf-8
from django.test.testcases import TestCase

from grading.models import *

class GradingTest(TestCase):

    def test_grade_calculation_no_weights(self):
        self.assertEqual(calculate_grade([1, 1, 1, 1]), 1)

    def test_grade_calculation_no_weights_range(self):
        self.assertEqual(calculate_grade(range(10)), 4.5)

    def test_grade_calculation(self):
        self.assertEqual(calculate_grade([1,1,1,2], [1, 1, 1, 3]), 1.5)
