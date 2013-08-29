# coding=utf-8
from django.http.request import HttpRequest
from django.test.testcases import TestCase
from grading.models import StudentGroup, GradeableActivity
from grading.views import GradeGroupActivity

class TestConversion(TestCase):

    fixtures = ['test_fixture.json']

    def setUp(self):
        r = HttpRequest()
        r.method = "get"
        args = []
        group = StudentGroup.objects.get(name = "group1")
        activity = GradeableActivity.objects.get(name = "test1")
        kwargs = {"group_id" : group.pk, "activity_id": activity.pk}
        view = GradeGroupActivity()
        view.request = r
        view.dispatch(r,*args, **kwargs)
        self.view = view
        self.activity = activity
        self.group = group


    def test_group_is_converted(self):
        self.assertEqual(self.view.group, self.group)

    def test_activity_is_converted(self):

        self.assertEqual(self.view.activity, self.activity)


