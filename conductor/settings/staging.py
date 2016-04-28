import os

from conductor.settings.base import *  # noqa

# FIXME: The wildcard is only here while testing on Vagrant.
# Host header checking fails without it.
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': '127.0.0.1',
    }
}

STATIC_ROOT = os.environ['STATIC_ROOT']
