from conductor.settings.base import *  # noqa

DEBUG = True

# Overwrite the values since development serves things from multiple ports.
CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
    'localhost:4000',
)
