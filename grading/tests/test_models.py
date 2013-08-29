# coding=utf-8
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from bd_checker_2.models import Student


class StudentTest(TestCase):

    def test_user_creation_creates_student(self):
        u = User.objects.create(username = "test1", email="foo@foo.pl")
        qs = Student.objects.filter(user=u)
        self.assertEqual(len(qs), 1)