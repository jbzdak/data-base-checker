# coding=utf-8
from django.forms.models import ModelForm
from django.forms import BooleanField
from grading.models import PartialGrade


class GradePartForm(ModelForm):

    def __init__(self,  grade_part, student, *args,  **kwargs):

        self.grade_part = grade_part
        self.student=student

        if "prefix" not in kwargs:
            kwargs['prefix'] = "s/{s.student.pk}/gp/{s.grade_part.pk}".format(s=self)
        super(GradePartForm, self).__init__(*args, **kwargs)

    def save(self, commit = True):
        new_grade = super(GradePartForm, self).save(commit = False)
        new_grade.student = self.student
        new_grade.grade_part = self.grade_part
        if commit:
            new_grade.save()
        return new_grade

    class Meta:
        model = PartialGrade
        fields = ['grade', 'short_description']