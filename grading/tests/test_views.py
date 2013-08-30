# coding=utf-8
from django.http.request import HttpRequest
from django.test import Client
from django.test.testcases import TestCase
from grading.models import StudentGroup, GradeableActivity
from grading.views import GradeGroupActivity

class BaseTest(TestCase):

    fixtures = ['test_fixture.json']

    def setUp(self):
        super(BaseTest, self).setUp()

        self.group = StudentGroup.objects.get(name = "group1")
        self.activity = GradeableActivity.objects.get(name = "test1")

class TestGradingViewInternals(BaseTest):

    fixtures = ['test_fixture.json']

    def setUp(self):
        super(TestGradingViewInternals, self).setUp()
        r = HttpRequest()
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

    def setUp(self):
        super(TestGradingView, self).setUp()
        self.c = Client()

    def test_view_does_not_raise(self):
        response = self.c.get("/grading/grade/group/1/acitvity/1")
        self.assertEqual(response.status_code, 200)
