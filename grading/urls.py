from django.conf.urls import patterns, include, url

from django.contrib import admin
from grading.views import GradeGroupActivity, ShowMyGrades

admin.autodiscover()

urlpatterns = patterns('grading.views',
    url(
        r'grade/course/(?P<group_id>\d+)/acitvity/(?P<activity_id>\d+)',
        GradeGroupActivity.as_view()
    ),
    url(
        r'my_grades',
        ShowMyGrades.as_view()
    ),
)
