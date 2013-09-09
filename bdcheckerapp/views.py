from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class TestSql(TemplateView):
    template_name = "test_sql.html"