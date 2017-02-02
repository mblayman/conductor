import os

from conductor.settings.base import *  # noqa

ALLOWED_HOSTS = [os.environ['DJANGO_ALLOWED_HOSTS']]

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
