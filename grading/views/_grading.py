from itertools import chain
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.list import ListView
from grading.forms import GradePartForm
from grading.models import Course, GradeableActivity, PartialGrade, StudentGrade
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from grading.models import Student
from grading.views._base import StudentView, LoginView

__all__ = [
    "GradeGroupActivity", "ShowMyGrades", "GradeActivityChooseCourse"
]

class GradeGroupActivity(LoginView, TemplateView):

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

        self.group = get_object_or_404(Course, pk=group_id)
        self.activity = get_object_or_404(GradeableActivity, pk=activity_id)

        self.grade_forms = self.__get_forms()

        return super(GradeGroupActivity, self).dispatch(request)

    def check_permissions(self):
        user = self.request.user

        if user.is_staff:
            if user.has_perm("grading.change_partialgrade") and user.has_perm("grading.change_student"):
                return True

        if user.has_perm("grading.can_see_students_data") and user.has_perm("grading.can_grade"):
            return True

        return False

    def post(self, request, *args, **kwargs):
        invalid_forms = False
        for form in self.__grade_forms_iter():
            if form.is_valid():
                form.save_if_needed()
            else:
                invalid_forms = True

        if invalid_forms:
            return self.get(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to=request.path)


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
            grade = StudentGrade.objects.get(student=st, activity=self.activity)
            grade_forms.append([
                st, activities_for_student, grade
            ])
        return grade_forms


    def get_context_data(self, **kwargs):
        context =  super(GradeGroupActivity, self).get_context_data(**kwargs)
        context.update({
            "grade_forms" : self.grade_forms,
            "activity": self.activity,
            "student_group": self.group

        })
        return context

class ShowMyGrades(StudentView, ListView):

    template_name = "grading/my_grades.html"

    model = StudentGrade

    def __init__(self, **kwargs):
        super(ShowMyGrades, self).__init__(**kwargs)
        self.request = None
        self.student = None

    def get_context_data(self, **kwargs):
        ctx = super(ShowMyGrades, self).get_context_data(**kwargs)
        ctx.update({
            "student": self.student
        })
        return ctx


    def get_queryset(self):
        return self.student.grades.all()

class GradeActivityChooseCourse(TemplateView):

    template_name = "grading/admin/choose_course_for_activity.html"


    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def dispatch(self, request, activity_id, *args, **kwargs):
        self.activity = get_object_or_404(GradeableActivity, pk=activity_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['activity'] = self.activity
        ctx['courses'] = self.activity.courses.all()
        return ctx

    def get(self, request, *args, **kwargs):
        if len(self.activity.courses.all()) == 1:
            course = self.activity.courses.all()[0]
            return redirect("grade-activity", group_id=course.pk, activity_id=self.activity.pk)
        return super().get(request, *args, **kwargs)