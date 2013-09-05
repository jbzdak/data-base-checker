from django.conf.urls import patterns, include, url

from bdchecker.views import SelectActivityView
urlpatterns = patterns('',
    url(
        r'select',
        SelectActivityView.as_view()
    )
)
