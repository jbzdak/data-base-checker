# coding=utf-8
from django.test.client import Client
from django.test.testcases import TestCase


class TestSelectActivity(TestCase):

    def setUp(self):
        super(TestSelectActivity, self).setUp()
        self.c = Client()

    def test_on_unloged_redirects_to_login_page(self):
        response = self.c.get("/bdchecker/select")
        self.assertEqual(response.status_code, 302)
