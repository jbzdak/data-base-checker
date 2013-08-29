# coding=utf-8
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from grading.models import Student, GradeableActivity
from grading.models._models import StudentGroup


class StudentTest(TestCase):

    def test_user_creation_creates_student(self):
        u = User.objects.create(username = "test1", email="foo@foo.pl")
        qs = Student.objects.filter(user=u)
        self.assertEqual(len(qs), 1)

class ActivityTest(TestCase):

    def test_sort_key_auto_set(self):
        a = GradeableActivity.objects.create(name="foo")
        self.assertEqual(a.sort_key, "foo")

class TestGrades(TestCase):

    def setUp(self):
        self.u = User.objects.create(username = "test1", email="foo@foo.pl")
        self.student =  Student.objects.filter(user=self.u).get()

        self.other_user = User.objects.create(username = "other", email="foo@foo.pl")
        self.other_student =Student.objects.filter(user=self.other_user).get()
        self.group = StudentGroup.objects.create(name = "group")
        self.other_group = StudentGroup.objects.create(name = "other_group")

        self.student.group = self.group
        self.student.save()
        self.other_student.group = self.other_group
        self.other_student.save()

        self.activity = GradeableActivity(name = "activity")
        self.activity.save()
        self.activity.groups.add(self.group)
        self.activity.save()

        self.otheractivity = GradeableActivity(name = "other")
        self.otheractivity.save()
        self.otheractivity.groups.add(self.other_group)
        self.otheractivity.save()



    def test_sync_grades_when_activity_is_added_to_group(self):

        # After setup it shpould be so:
        self.assertEqual(len(self.student.grades.all()), 1)
        #Other student shouldn't change
        self.assertEqual(len(self.other_student.grades.all()), 1)

        activity = GradeableActivity(name = "activity")
        activity.save()
        activity.groups.add(self.group)
        activity.save()

        #Now we should have two grades
        self.assertEqual(len(self.student.grades.all()), 2)
        #Other student shouldn't change
        self.assertEqual(len(self.other_student.grades.all()), 1)

        for g in self.student.grades.all():
            self.assertEqual(g.grade, 0.0)

    def test_sync_grades_when_student_is_added_to_group(self):
        u = User.objects.create(username = "test2", email="foo@foo.pl")
        student =  Student.objects.filter(user=u).get()

        # Before addition there should be no grades
        self.assertEqual(len(student.grades.all()), 0)
        student.group = self.group
        student.save()
        self.assertEqual(len(student.grades.all()), 1)



