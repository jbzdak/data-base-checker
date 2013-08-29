from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('grading.views',
    url(ur'^grade/group/(?P<group_id>\d+)/acitvity/(?P<activity_id>\d+)', ),
)
