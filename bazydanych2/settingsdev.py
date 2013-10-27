
from bazydanych2.settingsshared import *

DEBUG=True
TEMPLATE_DEBUG=True

STATIC_ROOT = '/tmp/staticfiles'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
         '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            "level": 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler'
        }
    },
    'root':{
        'handlers' : ['console']
    },
    'loggers': {

        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'bd',                      # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#        'TEST_NAME': ''
#    },
#    'zaj1db': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'zaj1db',                      # Or path to database file if using sqlite3.
#        'USER': 'bd',                      # Not used with sqlite3.
#        'PASSWORD': 'yorkambanmarfajakcofjenbaheishajlyishdipsEshtEcFoamOtgeybMoovTicHeukciedAdemmEchIdkabcoojHecwefDanLewElCubrEvsisujenyicpixJepNiv',                  # Not used with sqlite3.
#        'HOST': '192.168.56.10',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#        'TEST_NAME': 'zaj1_test'
#    }
#}

INSTALLED_APPS += ('celery_test_app', )