import os

from lcp.settings.base import *  # noqa

# FIXME: The wildcard is only here while testing on Vagrant.
# Host header checking fails without it.
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
