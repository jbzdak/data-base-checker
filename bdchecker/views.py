from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from grading.models import *

__all__ = ["SelectActivityView"]

class SelectActivityView(ListView):

    template_name = "bdchecker/select_activity.html"

    def __init__(self, **kwargs):
        super(SelectActivityView, self).__init__(**kwargs)
        self.student = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, user = self.request.user)
        return super(SelectActivityView, self).dispatch(request, *args,
                                                          **kwargs)

    def get_queryset(self):
        return GradeableActivity.objects.annotate(
            count = Count("grade_parts__bdchecker_part")
        ).filter(count__gt = 0, groups__students=self.student)

class PerformActivity(TemplateView):

    template_name = "bdchecker/base.html"