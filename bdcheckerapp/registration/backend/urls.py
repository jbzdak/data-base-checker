"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""


from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from bdcheckerapp.registration.backend.views import (
    BDRegistrationView, BDActivationView
)


urlpatterns = patterns('',
   url(r'^activate/complete/$',
       TemplateView.as_view(template_name='registration/activation_complete.html'),
       name='registration_activation_complete'),
   url(r'^activate/(?P<activation_key>\w+)/$',
       BDActivationView.as_view(),
       name='registration_activate'),
   url(r'^register/$',
       BDRegistrationView.as_view(),
       name='registration_register'),
   url(r'^register/complete/$',
       TemplateView.as_view(template_name='registration/registration_complete.html'),
       name='registration_complete'),
   url(r'^register/closed/$',
       TemplateView.as_view(template_name='registration/registration_closed.html'),
       name='registration_disallowed'),
   (r'', include('registration.auth_urls')),
)
