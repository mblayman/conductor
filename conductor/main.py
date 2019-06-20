import os
import sys

import django
from gunicorn.app import wsgiapp


def main() -> None:
    if len(sys.argv) > 1:
        manage = sys.argv[1] == "manage"
    else:
        manage = False

    if manage:
        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv[1:])
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
        django.setup()

        sys.argv.append("conductor.wsgi:application")
        wsgiapp.run()
