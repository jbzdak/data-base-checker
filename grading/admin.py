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
            'fields': ['sort_key']
        }),
    )

class GradePartInline(admin.TabularInline):
    model = GradePart

class ActivityAdmin(admin.ModelAdmin):
    inlines = [GradePartInline]

class UserInline(admin.StackedInline):
    model = get_user_model()
    fields = ('firtst_name', 'last_name', 'email')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'user__email', 'group')
    search_fields = list_display

    list_display_links = ('user__first_name', 'user__last_name', 'user__email')

    list_filter = ['group']
    list_editable = ['group']

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

admin.site.register(Student, StudentAdmin)
admin.site.register(StudentGroup, NamedSortableAdmin)
admin.site.register(GradeableActivity, ActivityAdmin)