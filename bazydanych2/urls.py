#from bdchecker.views import TestSql
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grading/', include("grading.urls")),
 #   url(r'test_sql', TestSql.as_view())
)
