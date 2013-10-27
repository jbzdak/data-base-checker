# -*- coding: utf-8 -*-

import  os

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

ATOMIC_REQUESTS = True
MANAGERS = ADMINS

DIRNAME = os.path.dirname(__file__)

ROOTDIR = os.path.split(DIRNAME)[0]

#Wszystkie materiały które nie są dostępne dla studentów
#ukryte są w tym katalogu znajdującym się poza repozytorium!
BD_AUTOGRADER_CONFIG_DIR = os.path.join(ROOTDIR, "bd_autograder_conf")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bd',                      # Or path to database file if using sqlite3.
        'USER': 'bd',                      # Not used with sqlite3.
        'PASSWORD': 'yorkambanmarfajakcofjenbaheishajlyishdipsEshtEcFoamOtgeybMoovTicHeukciedAdemmEchIdkabcoojHecwefDanLewElCubrEvsisujenyicpixJepNiv',                  # Not used with sqlite3.
        'HOST': '192.168.56.10',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_NAME': 'bd_test'
    },
    'zaj1db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zaj1db',                      # Or path to database file if using sqlite3.
        'USER': 'bd',                      # Not used with sqlite3.
        'PASSWORD': 'yorkambanmarfajakcofjenbaheishajlyishdipsEshtEcFoamOtgeybMoovTicHeukciedAdemmEchIdkabcoojHecwefDanLewElCubrEvsisujenyicpixJepNiv',                  # Not used with sqlite3.
        'HOST': '192.168.56.10',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_NAME': 'zaj1_test'
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Warsaw'

LOGIN_URL="/konto/login"

ACCOUNT_ACTIVATION_DAYS = 3

AUTOREGISTER_TO_COURSE = "group1"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'IdTokquagPhifnecFipJigtunVahiOmeckeyHedyeckoidUfekCypDihuerOlvEOvgauwokJajkecibHarEnIlbyekinIdcibnakquovCudquaphGiHaphuncypBagDu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bazydanych2.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bazydanych2.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'djcelery',
    'kombu.transport.django',
    'south',
    'grading',
    'registration',
    'bdcheckerapp'
)

# DJCELERY CONFIG

import djcelery
djcelery.setup_loader()

BROKER_URL = 'django://'

ZAJ1_DATABASE = "bdchecker_zaj1"