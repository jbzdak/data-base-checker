from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^login/', login,
        name="login", kwargs={
            "extra_context": {"form_header": "Zaloguj się!"}}),
    url(r'^logout', logout)
)

if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
