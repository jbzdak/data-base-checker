from django.conf.urls import patterns, include, url

from django.contrib import admin
from grading.views import *

admin.autodiscover()

urlpatterns = patterns('grading.views',
    url(
        r'grade/course/(?P<group_id>\d+)/acitvity/(?P<activity_id>\d+)',
        GradeGroupActivity.as_view(),
        name = "autograde-activity"
    ),
    url(
        r'my_grades',
        ShowMyGrades.as_view(),
        name="my-grades"
    ),
    url(r'autograde/(?P<grade_part>\d+)', GradeTask.as_view(), name="do-autograde"),
    url(r'autograde/view/(?P<pk>\d+)', GradingResult.as_view(), name="show-result"),
    url(r'activity/(?P<name>[\w\d\-]+)', GradeActivity.as_view(), name="activity"),
    url(r'course/(?P<name>[\w\d\-]+)', CourseView.as_view(), name="student-course")

)
