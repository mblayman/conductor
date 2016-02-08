from lcp.settings.base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
)


# Forcing migrations to run during testing is super annoying
# when the migration hasn't been generated yet.
# Skip migrations for tests.

class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()
