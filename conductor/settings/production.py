import os

from conductor.settings.base import *  # noqa

# Let's be clear that DEBUG is off.
DEBUG = False

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

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (  # noqa
    'rest_framework_json_api.renderers.JSONRenderer',
)
