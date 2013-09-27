#from bdchecker.views import TestSql
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grading/', include("grading.urls")),
    url(r'^konto/', include("bdcheckerapp.login_urls")),
    url(r'^register/', include('bdcheckerapp.registration.backend.urls'),),
)

if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
