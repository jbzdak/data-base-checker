# coding=utf-8
from django.contrib.auth.models import User, Group
from django.test.testcases import TestCase
from grading.models import *
from grading.autograding import get_autograders


class StudentTest(TestCase):

    def test_user_creation_creates_student(self):
        u = User.objects.create(username = "test1", email="foo@foo.pl")
        u.groups.add(Group.objects.get(name = "students"))
        u.save()
        qs = Student.objects.filter(user=u)
        self.assertEqual(len(qs), 1)

    def test_can_update_user(self):
        u = User.objects.create(username = "test1", email="foo@foo.pl")
        u.groups.add(Group.objects.get(name = "students"))
        u.save()
        u.email = "bar@bar.pl"
        u.save()

    def test_student_not_created_for_inactive_users(self):
        u = User.objects.create(username = "test1", email="foo@foo.pl", is_active=False)
        u.groups.add(Group.objects.get(name = "students"))
        u.save()
        qs = Student.objects.filter(user=u)
        self.assertEqual(len(qs), 0)

    def test_student_not_created_for_staff_users(self):
        u = User.objects.create(username = "test1", email="foo@foo.pl", is_staff=True)
        u.groups.add(Group.objects.get(name = "students"))
        u.save()
        qs = Student.objects.filter(user=u)
        self.assertEqual(len(qs), 0)



class ActivityTest(TestCase):

    def test_sort_key_auto_set(self):
        a = GradeableActivity.objects.create(name="foo")
        self.assertEqual(a.sort_key, "foo")

class TestFixture(TestCase):

    def setUp(self):
        self.u = User.objects.create(username = "test1", email="foo@foo.pl")
        self.u.groups.add(Group.objects.get(name = "students"))
        self.u.save()
        self.student =  Student.objects.filter(user=self.u).get()

        self.other_user = User.objects.create(username = "other", email="foo@foo.pl")
        self.other_user.groups.add(Group.objects.get(name = "students"))
        self.other_user.save()

        self.other_student =Student.objects.filter(user=self.other_user).get()
        self.group = Course.objects.create(name = "course")
        self.other_group = Course.objects.create(name = "other_group")

        self.student.course = self.group
        self.student.save()
        self.other_student.course = self.other_group
        self.other_student.save()

        self.activity = GradeableActivity(name = "activity")
        self.activity.save()
        self.activity.courses.add(self.group)
        self.activity.save()

        self.otheractivity = GradeableActivity(name = "other")
        self.otheractivity.save()
        self.otheractivity.courses.add(self.other_group)
        self.otheractivity.save()


class TestGrades(TestFixture):

    def test_sync_grades_when_activity_is_added_to_group(self):

        # After setup it shpould be so:
        self.assertEqual(len(self.student.grades.all()), 1)
        #Other student shouldn't change
        self.assertEqual(len(self.other_student.grades.all()), 1)

        activity = GradeableActivity(name = "activity2")
        activity.save()
        activity.courses.add(self.group)
        activity.save()

        #Now we should have two grades
        self.assertEqual(len(self.student.grades.all()), 2)
        #Other student shouldn't change
        self.assertEqual(len(self.other_student.grades.all()), 1)

        for g in self.student.grades.all():
            self.assertEqual(g.grade, 2.0)

    def test_sync_grades_when_student_is_added_to_group(self):
        u = User.objects.create(username = "test2", email="foo@foo.pl")
        u.groups.add(Group.objects.get(name = "students"))
        u.save()
        student =  Student.objects.filter(user=u).get()

        # Before addition there should be no grades
        self.assertEqual(len(student.grades.all()), 0)
        student.course = self.group
        student.save()
        self.assertEqual(len(student.grades.all()), 1)



class TestGrading(TestFixture):

    def setUp(self):
        super(TestGrading, self).setUp()

        self.grade_part_1 = GradePart.objects.create(
            weight = 1,
            required = True,
            activity = self.activity,
            name = "Zadanie 1"

        )
        self.grade_part_2 =  GradePart.objects.create(
            weight = 2,
            required = False,
            activity = self.activity,
            name = "Zadanie 2"
        )

        self.activity.default_grade = 812.0
        self.activity.save()


    def test_default_grade_retuended_when_all_activities_unfinished(self):

        sg = StudentGrade()
        grade_student(self.activity, self.student, sg)
        self.assertEqual(sg.grade, 812.0)
        self.assertIn('Zadanie 1', sg.short_description)

    def test_default_grade_retuended_when_required_activities_unfinished(self):

        PartialGrade.objects.create(
           student = self.student,
           grade = 5.0,
           grade_part = self.grade_part_2
        )

        sg = StudentGrade()
        grade_student(self.activity, self.student, sg)

        self.assertEqual(sg.grade, 812.0)
        self.assertIn('Zadanie 1', sg.short_description)

    def test_grade_calculated_when_all_required_activitees_finished(self):

        PartialGrade.objects.create(
           student = self.student,
           grade = 5.0,
           grade_part = self.grade_part_1
        )

        sg = StudentGrade()
        grade_student(self.activity, self.student, sg)

        self.assertEqual(sg.grade, 3)

    def test_grade_calculated_when_all_activities_finished(self):

        PartialGrade.objects.create(
           student = self.student,
           grade = 3,
           grade_part = self.grade_part_2
        )

        PartialGrade.objects.create(
           student = self.student,
           grade = 3.0,
           grade_part = self.grade_part_1
        )

        sg = StudentGrade()
        grade_student(self.activity, self.student, sg)

        self.assertEqual(sg.grade, 3)

    def test_default_grade_returned_when_regired_activity_has_grade_below_passing(self):

        PartialGrade.objects.create(
           student = self.student,
           grade = 3,
           grade_part = self.grade_part_2
        )

        PartialGrade.objects.create(
           student = self.student,
           grade = 2,
           grade_part = self.grade_part_1
        )

        sg = StudentGrade()
        grade_student(self.activity, self.student, sg)

        self.assertEqual(sg.grade, 812.0)

    def test_grade_gets_updated(self):

       PartialGrade.objects.create(
           student = self.student,
           grade = 5.0,
           grade_part = self.grade_part_1
       )

       self.assertEqual(StudentGrade.objects.get(student=self.student, activity=self.activity).grade, 3)

    def test_grade_gets_updated_if_we_add_new_grade_part(self):
        #Updates the database so grade is calculated
        self.test_grade_calculated_when_all_activities_finished()
        #Sanity check

        sg = StudentGrade()
        grade_student(self.activity, self.student, sg)

        self.assertNotEqual(sg.grade, 812.0)

        GradePart.objects.create(
            name = "test-xxx",
            required = True,
            activity = self.activity,
        )

        sg = StudentGrade()
        grade_student(self.activity, self.student, sg)
        self.assertEqual(sg.grade, 812.0)

class TestAutogradeableGradePart(TestFixture):

    def test_name_is_set(self):
        model = AutogradeableGradePart.objects.create(
            activity = self.activity,
            autograding_controller = get_autograders()['test']
        )
        self.assertEqual(model.name, model.autograding_controller)