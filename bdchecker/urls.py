from django.conf.urls import patterns, include, url

from bdchecker.views import SelectActivityView, PerformActivity

urlpatterns = patterns('',
    url(
        r'select',
        SelectActivityView.as_view()
    ),
    url(
        r'perform/(?P<activity_id>\d+)',
        PerformActivity.as_view(),
        name="perform-activity"
    )
)
