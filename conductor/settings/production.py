from conductor.settings.base import *  # noqa

# Let's be clear that DEBUG is off.
DEBUG = False

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

SILENCED_SYSTEM_CHECKS = [
    # HSTS is set with the Nginx load balancer so the app server
    # does not need to add that header.
    'security.W004',
    # SSL redirection is handled at the load balancer.
    'security.W008',
]
