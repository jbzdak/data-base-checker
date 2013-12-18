from django.contrib.auth import get_user_model
from django.contrib import admin, messages

# Register your models here.
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

from grading.models import *

class NamedSortableAdmin(admin.ModelAdmin):

    prepopulated_fields = {
        "slug_field" : ["name"]
    }

    list_display = ["name"]

class GradePartInline(admin.TabularInline):
    model = GradePart


class ActivityAdmin(NamedSortableAdmin):

    inlines = [GradePartInline]


    def grade_activity(self, request, qs):
        if len(qs) != 1:
            messages.warning(request, ugettext("Select only one activity"))
            return None
        act = qs[0]
        courses = act.courses.all()

        if len(courses) == 0:
            messages.warning(request, ugettext("Activity is not attached to any course"))

        if len(courses) == 1:
            return redirect("grade-activity", activity_id=act.pk, group_id=courses[0].pk)

        return redirect("grade-activity-select-course", activity_id=act.pk)

    grade_activity.short_description = ugettext_lazy('Grade this activity')

    actions = [grade_activity]


class UserInline(admin.StackedInline):
    model = get_user_model()
    fields = ('firtst_name', 'last_name', 'email')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'course')
    search_fields = list_display

    list_display_links = ('user__username', 'user__first_name', 'user__last_name', 'user__email')

    list_filter = ['course']
    list_editable = ['course']

    def user__first_name(self, obj):
        return obj.user.first_name

    user__first_name.short_description = "First name"
    user__first_name.admin_order_field  = "user__first_name"

    def user__last_name(self, obj):
        return obj.user.last_name

    user__last_name.short_description = "Last name"
    user__last_name.admin_order_field = "user__username"

    def user__email(self, obj):
        return obj.user.email

    user__email.short_description = "Email"
    user__email.admin_order_field = "user__email"

    def user__username(self, obj):
        return obj.user.username

    user__username.short_description = "Username"
    user__username.admin_order_field = "user__username"

class StudentGradeAdmin(admin.ModelAdmin):

    list_display = ('grade', 'student__user__first_name', 'student__user__last_name', 'student__user__email', 'activity__name')
    search_fields = list_display

    list_display_links = list_display

    list_filter = ['student__course', 'activity__name']

    def student__user__first_name(self, obj):
        return obj.student.user.first_name

    student__user__first_name.short_description = "First name"
    student__user__first_name.admin_order_field  = "student__user__first_name"

    def activity__name(self, obj):
        return obj.activity.name

    activity__name.short_description = "Activity name"
    activity__name.admin_order_field = "activity__names"

    def student__user__last_name(self, obj):
        return obj.student.user.last_name

    student__user__last_name.short_description = "Last name"
    student__user__last_name.admin_order_field = "student__user__username"

    def student__user__email(self, obj):
        return obj.student.user.email

    student__user__email.short_description = "Email"
    student__user__email.admin_order_field = "student__user__email"


class AutoGraderGradePartAdmin(admin.TabularInline):
    model = AutogradeableGradePart
    fields = ['pk', 'autograding_controller', 'name', 'sort_key', 'weight', 'required']
    readonly_fields = ['pk']
    ordering = ["sort_key"]

class AutogradeableActivityAdmin(NamedSortableAdmin):
    inlines = [
        AutoGraderGradePartAdmin
    ]

class AutogradingResultAdmin(admin.ModelAdmin):

    list_display = [
        'student__user__username', 'grade', 'grade_part', 'is_current', 'view_link'
    ]

    list_filter = ['is_current', 'student__user__username', 'grade_part__activity__name', 'grade_part__name']

    def student__user__username(self, obj):
        return obj.student.user.username

    student__user__username.short_description = "Username"
    student__user__username.admin_order_field = "student__user__username"

    def view_link(self, obj):
        if obj.autograder_input:
            return mark_safe(
                '<a href="{}">view student\'s input</a>'.format(
                reverse('view-student-input', kwargs={'pk':obj.pk})))
        else:
            return "Student input not recoverable"


admin.site.register(AutogradedActivity, AutogradeableActivityAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentGrade, StudentGradeAdmin)
admin.site.register(Course, NamedSortableAdmin)
admin.site.register(GradeableActivity, ActivityAdmin)
admin.site.register(AutogradingResult, AutogradingResultAdmin)