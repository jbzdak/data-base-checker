from itertools import chain
from django.shortcuts import render

# Create your views here.
from grading.forms import GradePartForm
from grading.models._models import StudentGroup, GradeableActivity, PartialGrade
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView


class GradeGroupActivity(TemplateView):

    template_name = "grading/grade_group_activity.html"

    def __init__(self, **kwargs):
        super(GradeGroupActivity, self).__init__(**kwargs)
        self.group = None
        self.activity = None
        self.request = None
        self.grade_forms = None

    def dispatch(self, request, group_id, activity_id):

        self.group = get_object_or_404(StudentGroup, pk=group_id)
        self.activity = get_object_or_404(GradeableActivity, pk=activity_id)

        self.grade_forms = self.__get_forms()

        return super(GradeGroupActivity, self).dispatch(request)


    def post(self, request, *args, **kwargs):
        for form in self.__grade_forms_iter():
            if form.is_valid():
                form.save_if_needed()
        return self.get(request, *args, **kwargs)


    def __grade_forms_iter(self):
        forms = [row[1] for row in self.grade_forms]
        return chain(*forms)


    def __get_forms(self):
        grade_forms = []
        for st in self.group.students.all():
            activities_for_student = []
            for gp in self.activity.grade_parts.all():
                data = None
                if self.request.method.lower() == 'post':
                    data = self.request.POST
                instance = None
                try:
                    instance = PartialGrade.objects.get(student=st, grade_part=gp)
                except PartialGrade.DoesNotExist as e:
                    pass
                form = GradePartForm(gp, st, data=data, instance=instance)
                activities_for_student.append(form)
            grade_forms.append([
                st, activities_for_student
            ])
        return grade_forms


    def get_context_data(self, **kwargs):
        context =  super(GradeGroupActivity, self).get_context_data(**kwargs)
        context.update({
            "grade_forms" : self.grade_forms,

        })
        return context



