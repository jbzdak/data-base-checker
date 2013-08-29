# coding=utf-8
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from grading.models import Student, GradeableActivity


class StudentTest(TestCase):

    def test_user_creation_creates_student(self):
        u = User.objects.create(username = "test1", email="foo@foo.pl")
        qs = Student.objects.filter(user=u)
        self.assertEqual(len(qs), 1)

class ActivityTest(TestCase):

    def test_sort_key_auto_set(self):
        a = GradeableActivity.objects.create(name="foo")
        self.assertEqual(a.sort_key, "foo")

