# coding=utf-8
from django.test.client import Client
from django.test.testcases import TestCase
from grading.models._models import Student


class TestSelectActivity(TestCase):

    fixtures = [
        'bdchecker_test_fixture.json'
    ]

    def setUp(self):
        super(TestSelectActivity, self).setUp()
        self.c = Client()

    def test_on_unloged_redirects_to_login_page(self):
        response = self.c.get("/bdchecker/select")
        self.assertEqual(response.status_code, 302)

    def test_user_without_student_gets_404(self):
        Student.objects.filter(user__username = 'no-student').delete()
        authenticated = self.c.login(username="no-student", password="foo")
        self.assertTrue(authenticated, "Cant login")
        response = self.c.get("/bdchecker/select")
        self.assertEqual(response.status_code, 404)

    def test_response_content(self):
        authenticated = self.c.login(username="test-student", password="foo")
        self.assertTrue(authenticated, "Cant login")
        response = self.c.get("/bdchecker/select")
        self.assertEqual(response.status_code, 200)
        self.assertIn("""<a href="/bdchecker/perform/3">Zajęcia 1 (testowe)</a>""", str(response))