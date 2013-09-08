from django.contrib.auth import get_user_model
from django.contrib import admin

# Register your models here.

from grading.models import *

class NamedSortableAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ['name']
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ['sort_key', "slug_field"]
        }),
    )

    prepopulated_fields = {
        "slug_field" : ["name"]
    }

class GradePartInline(admin.TabularInline):
    model = GradePart

class ActivityAdmin(admin.ModelAdmin):
    inlines = [GradePartInline]

class UserInline(admin.StackedInline):
    model = get_user_model()
    fields = ('firtst_name', 'last_name', 'email')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'user__email', 'course')
    search_fields = list_display

    list_display_links = ('user__first_name', 'user__last_name', 'user__email')

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
    fields = ['pk', 'autograding_controller', 'name', 'weight', 'required']
    readonly_fields = ['pk']

class AutogradeableActivityAdmin(admin.ModelAdmin):
    inlines = [
        AutoGraderGradePartAdmin
    ]

admin.site.register(AutogradedActivity, AutogradeableActivityAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentGrade, StudentGradeAdmin)
admin.site.register(Course, NamedSortableAdmin)
admin.site.register(GradeableActivity, ActivityAdmin)