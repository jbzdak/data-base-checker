# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from sqlalchemy.types import default
from bdcheckerapp.models import Team
from grading.models._models import Course, GradeableActivity, GradePart, AutogradeableGradePart, PartialGrade, AutogradingResult
from grading.tests.test_utils import create_student


class TestFixture(TestCase):

    def setUp(self):

        self.course = Course.objects.create(name="foo")
        self.student_a = create_student(self.course)[1]
        self.student_b = create_student(self.course)[1]
        self.student_c = create_student(self.course)[1]
        self.student_d = create_student(self.course)[1]

        self.default_grade_aa = 812

        self.activity_a = GradeableActivity.objects.create(
            name="foo-act-1", default_grade=self.default_grade_aa)
        self.activity_a.courses.add(self.course)
        self.activity_a.save()
        self.grade_part_aa = AutogradeableGradePart.objects.create(
            activity = self.activity_a,
            name = "foo-act-1-a",
            autograding_controller = "test",
        )
        self.grade_part_ab = AutogradeableGradePart.objects.create(
            activity = self.activity_a,
            name = "foo-act-1-b",
            autograding_controller = "test"
        )
        self.activity_b = GradeableActivity.objects.create(
            name="foo-act-2", default_grade = self.default_grade_aa)
        self.activity_b.courses.add(self.course)
        self.activity_b.save()
        self.grade_part_ba = GradePart.objects.create(
            activity = self.activity_b,
            name = "foo-act-2-a",
        )
        self.grade_part_bb = GradePart.objects.create(
            activity = self.activity_b,
            name = "foo-act-2-b",
        )

        self.team_aba = Team.objects.create(
            student_1=self.student_a, student_2=self.student_b,
            activity=self.activity_a)
        self.team_acb = Team.objects.create(
            student_1=self.student_c, student_2=self.student_a,
            activity=self.activity_b)

    def assert_partial_grade(self, grade, student, grade_part):
        try:
            gp = PartialGrade.objects.get(student=student, grade_part=grade_part)
        except PartialGrade.DoesNotExist:
            self.assertEqual(grade, grade_part.default_grade)
            return None
        self.assertEqual(grade, gp.grade)
        return gp

class TestTeamManager(TestFixture):

    def test_get_team(self):
        self.assertEqual(Team.objects.get_team_for_student(
            self.student_a, self.activity_a), self.team_aba)

    def test_get_team_2(self):
        self.assertEqual(Team.objects.get_team_for_student(
            self.student_b, self.activity_a), self.team_aba)

    def test_get_other_student(self):
        self.assertEqual(Team.objects.get_other_student(
            self.student_a, self.activity_a), self.student_b)

    def test_get_other_student_2(self):
        self.assertEqual(Team.objects.get_other_student(self.student_b, self.activity_a), self.student_a)

    def test_get_all_teams_1(self):
        teams = Team.objects.all_teams_for_student(
            self.student_a)
        self.assertEqual(len(teams), 2)
        self.assertIn(self.team_aba, teams)
        self.assertEqual(len(teams), 2)
        self.assertIn(self.team_acb, teams)

    def test_get_all_teams_2(self):
        teams = Team.objects.all_teams_for_student(self.student_b)
        self.assertEqual(len(teams), 1)
        self.assertIn(self.team_aba, teams)

class TestTeamInAutograding(TestFixture):

    def test_student_outside_of_team(self):
        #Sanity check
        self.assert_partial_grade(
            self.default_grade_aa, self.student_a, self.grade_part_aa)
        self.assert_partial_grade(
            self.default_grade_aa, self.student_b, self.grade_part_aa)

        GradePart.objects.grade(self.grade_part_aa, self.student_d, 5.0, "OK")

        #Sanity check
        self.assert_partial_grade(5.0, self.student_d, self.grade_part_aa)

        #Test other
        self.assert_partial_grade(
            self.default_grade_aa, self.student_a, self.grade_part_aa)
        self.assert_partial_grade(
            self.default_grade_aa, self.student_b, self.grade_part_aa)

    def test_student_in_team(self):
        #Sanity check
        tested_grade_part = self.grade_part_aa

        self.assert_partial_grade(
            self.default_grade_aa, self.student_a, tested_grade_part)
        self.assert_partial_grade(
            self.default_grade_aa, self.student_b, tested_grade_part)

        GradePart.objects.grade(tested_grade_part, self.student_a, 5.0, "OK")

        #Sanity check
        self.assert_partial_grade(5.0, self.student_a, tested_grade_part)

        #Test teammember
        self.assert_partial_grade(5.0, self.student_b, tested_grade_part)

        self.assertEqual(len(PartialGrade.objects.all()), 2)

        #Test other
        self.assert_partial_grade(
            self.default_grade_aa, self.student_c, tested_grade_part)
        self.assert_partial_grade(
            self.default_grade_aa, self.student_d, tested_grade_part)

    def test_student_in_team_2(self):
        tested_grade_part = self.grade_part_ba

        self.assert_partial_grade(
            self.default_grade_aa, self.student_a, tested_grade_part)
        self.assert_partial_grade(
            self.default_grade_aa, self.student_b, tested_grade_part)

        GradePart.objects.grade(tested_grade_part, self.student_c, 5.0, "OK")

        #Sanity check
        self.assert_partial_grade(5.0, self.student_c, tested_grade_part)

        #Test teammember
        self.assert_partial_grade(5.0, self.student_a, tested_grade_part)

        self.assertEqual(len(PartialGrade.objects.all()), 2)

        #Test other
        self.assert_partial_grade(
            self.default_grade_aa, self.student_b, tested_grade_part)
        self.assert_partial_grade(
            self.default_grade_aa, self.student_d, tested_grade_part)

    def test_student_autograded(self):
        tested_grade_part = self.grade_part_aa

        self.assert_partial_grade(
            self.default_grade_aa, self.student_a, tested_grade_part)
        self.assert_partial_grade(
            self.default_grade_aa, self.student_b, tested_grade_part)

        AutogradingResult.objects.create(
            grade = 5,
            student = self.student_a,
            grade_part = tested_grade_part
        )

        AutogradingResult.objects.get(
            student = self.student_b,
            grade_part = tested_grade_part
        )

        self.assertEqual(len(AutogradingResult.objects.all()), 2)

        self.assert_partial_grade(5, self.student_a, tested_grade_part)
        self.assert_partial_grade(5, self.student_b, tested_grade_part)

        self.assertEqual(len(PartialGrade.objects.all()), 2)

