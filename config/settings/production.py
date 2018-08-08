from config.settings.base import *  # noqa

# Let's be clear that DEBUG is off.
DEBUG = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

SILENCED_SYSTEM_CHECKS = [
    # HSTS is set with the Nginx load balancer so the app server
    # does not need to add that header.
    'security.W004',
    # SSL redirection is handled at the load balancer.
    'security.W008',
]

# django-storages

AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'college-conductor'
