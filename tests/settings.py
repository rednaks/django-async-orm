"""Django settings."""
# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

# import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-%n*2l!dqp6wxjnz4kgv5y=2m6en@l495gb9@&$#o89%8oy75g'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': ':memory:',
        'TEST': {
            'NAME': 'testdb.sqlite3',
        },
        'OPTIONS': {
            'timeout': 5 
        }
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = [
    'django_async_orm.apps.AsyncOrmConfig',
    'tests',
]

MIDDLEWARE = [
]


SITE_ID = 1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
