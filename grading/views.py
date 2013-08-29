from django.shortcuts import render

# Create your views here.
from grading.models._models import StudentGroup, GradeableActivity
from shortcuts import get_object_or_404
from views.generic.base import TemplateView


class GradeGroupActivity(TemplateView):

    template_name = "grading/grade_group_activity.html"

    def dispatch(self, request, group_id, activity_id):

        self.group = get_object_or_404(StudentGroup, pk=group_id)
        self.activity = get_object_or_404(GradeableActivity, pk=activity_id)
        return super(GradeGroupActivity, self).dispatch(request)