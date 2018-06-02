from conductor.settings.base import *  # noqa

DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += ('debug_toolbar',)  # noqa
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa

# Overwrite the values since development serves things from multiple ports.
CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
    'localhost:4000',
)
