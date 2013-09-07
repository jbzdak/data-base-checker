# coding=utf-8
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.test import Client
from django.test.testcases import TestCase
from grading.models import Course, GradeableActivity
from grading.models._models import PartialGrade, StudentGrade
from grading.views import GradeGroupActivity

class BaseTest(TestCase):

    fixtures = ['grading_test.json']

    def setUp(self):
        super(BaseTest, self).setUp()

        self.group = Course.objects.get(name = "group1")
        self.activity = GradeableActivity.objects.get(name = "test1")
        self.c = Client()

class TestGradingViewInternals(BaseTest):

    fixtures = ['grading_test.json']

    def setUp(self):
        super(TestGradingViewInternals, self).setUp()
        r = HttpRequest()
        r.user = User.objects.get(username = "teacher")
        r.method = "get"
        args = []
        kwargs = {"group_id" : self.group.pk, "activity_id": self.activity.pk}
        view = GradeGroupActivity()
        view.request = r
        view.dispatch(r,*args, **kwargs)

        self.view = view


    def test_group_is_converted(self):

        self.assertEqual(self.view.group, self.group)

    def test_activity_is_converted(self):

        self.assertEqual(self.view.activity, self.activity)

    def test_context(self):
        ctx = self.view.get_context_data()
        self.assertIsNotNone(ctx)
        self.assertIn("grade_forms", ctx)
        self.assertEqual(len(ctx["grade_forms"]), 2)

class TestGradingView(BaseTest):


    def test_view_requires_login(self):
        response = self.c.get("/grading/grade/course/1/acitvity/1")
        self.assertEqual(response.status_code, 302)

    def test_view_rejects_user_without_perms(self):
        authenticated = self.c.login(username="no-permission", password="foo")
        self.assertTrue(authenticated, "Cant login")
        response = self.c.get("/grading/grade/course/1/acitvity/1")
        self.assertEqual(response.status_code, 403)

    def test_user_with_permissions(self):
        authenticated = self.c.login(username="teacher", password="foo")
        self.assertTrue(authenticated, "Cant login")
        response = self.c.get("/grading/grade/course/1/acitvity/1")
        self.assertEqual(response.status_code, 200)

    def test_full_update(self):
        gp = PartialGrade.objects.get(student__pk = 1, grade_part__pk=2)
        self.assertNotEqual(gp.grade, 5)
        authenticated = self.c.login(username="teacher", password="foo")
        self.assertTrue(authenticated, "Cant login")
        response = self.c.post(
            "/grading/grade/course/1/acitvity/1",
            data = {
                "s-1-gp-2-grade":"5",
                "s-1-gp-2-short_description":"",
                "s-1-gp-3-grade":"5",
                "s-1-gp-3-short_description":"dsa",
                "s-1-gp-4-grade":"5.00",
                "s-1-gp-4-short_description":"21",
                "s-4-gp-2-grade":"5",
                "s-4-gp-2-short_description":"312",
                "s-4-gp-3-grade":"5",
                "s-4-gp-3-short_description":"32",
                "s-4-gp-4-grade":"5"
            }
        )
        self.assertEqual(response.status_code, 302)
        gp = PartialGrade.objects.get(student__pk = 1, grade_part__pk=2)
        self.assertEqual(gp.grade, 5)

    def test_partial_upgrade(self):
        authenticated = self.c.login(username="teacher", password="foo")
        self.assertTrue(authenticated, "Cant login")

        gp = PartialGrade.objects.get(student__pk = 1, grade_part__pk=2)
        self.assertNotEqual(gp.grade, 5)
        grade_not_modified = PartialGrade.objects.get(student__pk = 1, grade_part__pk=3)
        response = self.c.post(
            "/grading/grade/course/1/acitvity/1",
            data = {
                "s-1-gp-2-grade":"5",
                "s-1-gp-2-short_description":"",
            }
        )
        self.assertEqual(response.status_code, 302, str(response))
        gp = PartialGrade.objects.get(student__pk = 1, grade_part__pk=2)
        self.assertEqual(gp.grade, 5)
        grade_not_modified_after_change = PartialGrade.objects.get(student__pk = 1, grade_part__pk=3)
        self.assertEqual(grade_not_modified.grade, grade_not_modified_after_change.grade)

    def test_grade_gets_updated_during_full_update(self):
        sg = StudentGrade.objects.get(student__pk = 1, activity__pk=1)
        self.assertNotEqual(float(sg.grade), 5)
        authenticated = self.c.login(username="teacher", password="foo")
        self.assertTrue(authenticated, "Cant login")
        response = self.c.post(
            "/grading/grade/course/1/acitvity/1",
            data = {
                "s-1-gp-2-grade":"5",
                "s-1-gp-2-short_description":"",
                "s-1-gp-3-grade":"5",
                "s-1-gp-3-short_description":"dsa",
                "s-1-gp-4-grade":"5.00",
                "s-1-gp-4-short_description":"21",
                "s-4-gp-2-grade":"5",
                "s-4-gp-2-short_description":"312",
                "s-4-gp-3-grade":"5",
                "s-4-gp-3-short_description":"32",
                "s-4-gp-4-grade":"5"
            }
        )
        self.assertEqual(response.status_code, 302)
        sg = StudentGrade.objects.get(student__pk = 1, activity__pk=1)
        self.assertEqual(float(sg.grade), 5)

    def test_zero_grade(self):
        sg = StudentGrade.objects.get(student__pk = 1, activity__pk=1)
        self.assertNotEqual(float(sg.grade), 2.0)
        authenticated = self.c.login(username="teacher", password="foo")
        self.assertTrue(authenticated, "Can't login")
        response = self.c.post(
            "/grading/grade/course/1/acitvity/1",
            data = {
                "s-1-gp-2-grade":"0",
                "s-1-gp-2-short_description":"das",
                "s-1-gp-3-grade":"5",
                "s-1-gp-3-short_description":"dsa",
                "s-1-gp-4-grade":"5.00",
                "s-1-gp-4-short_description":"21",
                "s-4-gp-2-grade":"5",
                "s-4-gp-2-short_description":"312",
                "s-4-gp-3-grade":"5",
                "s-4-gp-3-short_description":"32",
                "s-4-gp-4-grade":"5"
            }
        )
        self.assertEqual(response.status_code, 302)
        sg = StudentGrade.objects.get(student__pk = 1, activity__pk=1)
        self.assertEqual(float(sg.grade), 2.0)

class TestAutogradingGradeView(BaseTest):

    def test_proper_status(self):
        authenticated = self.c.login(username="teacher", password="foo")
        self.assertTrue(authenticated, "Cant login")
        response = self.c.get('/grading/autograde/5')
        self.assertEqual(response.status_code, 200)