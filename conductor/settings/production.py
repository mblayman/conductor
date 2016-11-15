import os

from conductor.settings.base import *  # noqa

# Let's be clear that DEBUG is off.
DEBUG = False

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

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (  # noqa
    'rest_framework_json_api.renderers.JSONRenderer',
)

EMAIL_BACKEND = 'anymail.backends.mailgun.MailgunBackend'

SILENCED_SYSTEM_CHECKS = [
    # HSTS is set with the Nginx load balancer so the app server
    # does not need to add that header.
    'security.W004',
    # SSL redirection is handled at the load balancer.
    'security.W008',
]
