from django.contrib import admin

# Register your models here.
from bdcheckerapp.models import Team


class TeamAdmin(admin.ModelAdmin):

    list_display = ['student1', 'student2', 'activity']

    search_fields = [
        'student_1__user__last_name', 'student_2__user',
        'student_1__user__first_name', 'student_2__first__last_name',
        'activity__name'
        ]

    list_filter = ['activity']

    def student1(self, obj):
        return str(obj.student_1)
    
    student1.short_description = "Student1"
    student1.admin_order_field = "student_1__user__username"
    
    def student2(self, obj):
        return str(obj.student_2)
    
    student2.short_description = "Student2"
    student2.admin_order_field = "student_2__user__username"

    def activity(self, obj):
        return obj.actity.name

    activity.short_description = "Zajęcia"
    activity.admin_order_field = "actity__name"

admin.site.register(Team, TeamAdmin)