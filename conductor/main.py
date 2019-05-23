import os
import sys

import django
from gunicorn.app import wsgiapp


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
    django.setup()

    sys.argv.append("conductor.wsgi:application")
    wsgiapp.run()
