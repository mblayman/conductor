import os

from conductor.settings.base import *  # noqa

ALLOWED_HOSTS = [os.environ['DJANGO_ALLOWED_HOSTS']]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': '127.0.0.1',
    }
}
