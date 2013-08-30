from itertools import chain
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
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

    @method_decorator(login_required)
    def dispatch(self, request, group_id, activity_id):

        if not self.check_permissions():
            return HttpResponse(status=403)

        self.group = get_object_or_404(StudentGroup, pk=group_id)
        self.activity = get_object_or_404(GradeableActivity, pk=activity_id)

        self.grade_forms = self.__get_forms()

        return super(GradeGroupActivity, self).dispatch(request)

    def check_permissions(self):
        user = self.request.user

        if user.is_staff:
            return user.has_perm("grading.change_partialgrade") and user.has_perm("grading.change_student")

        if user.has_perm("grading.can_see_students_data") and user.has_perm("grading.can_grade"):
            return True

        return False

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



