# coding=utf-8
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from grading.models import PartialGrade
from django.utils.translation import ugettext_lazy as _

class GradePartForm(ModelForm):

    def __init__(self,  grade_part, student, *args,  **kwargs):

        self.grade_part = grade_part
        self.student=student

        self.needs_save = False

        if "prefix" not in kwargs:
            kwargs['prefix'] = "s-{s.student.pk}-gp-{s.grade_part.pk}".format(s=self)

        super(GradePartForm, self).__init__(*args, **kwargs)

        self.fields['grade'].required = False

        self.fields['grade'].widget.attrs.update({
            "placeholder": _("Grade"),
            "size": 3
        })
        self.fields['short_description'].widget.attrs.update({
            "placeholder": _("Grade description"),

        })

    def clean(self):
        cleaned_data = super(GradePartForm, self).clean()
        if 'short_description' in cleaned_data and not 'grade' in cleaned_data:
            raise ValidationError(
                _("If short description is set you should also set grade", code="descr-no-grade")
            )
        self.needs_save = False
        if cleaned_data.get('grade', None):
            self.needs_save = True
        return cleaned_data

    def save_if_needed(self):
        if self.needs_save:
            self.save()

    def __mark_changed(self):
        self.fields['grade'].widget.attrs.update({
            "class": "changed"
        })
        self.fields['short_description'].widget.attrs.update({
             "class": "changed"
        })

    def save(self, commit = True):
        old_instance = None
        if self.instance.pk:
            old_instance = PartialGrade.objects.get(pk = self.instance.pk)
        new_grade = super(GradePartForm, self).save(commit = False)
        new_grade.student = self.student
        new_grade.grade_part = self.grade_part
        if commit:
            new_grade.save()
        if old_instance is None:
            self.__mark_changed()
        if old_instance and old_instance.grade != new_grade.grade or old_instance.short_description != new_grade.short_description:
            self.__mark_changed()
        return new_grade

    class Meta:
        model = PartialGrade
        fields = ['grade', 'short_description']


