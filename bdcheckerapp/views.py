from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from grading.models._models import Student


class TestSql(TemplateView):
    template_name = "test_sql.html"

class LandingPage(TemplateView):

    template_name = "landing_page.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        student = None
        try:
            student = user.student
        except Student.DoesNotExist:
            pass

        return super().get_context_data(**kwargs)



