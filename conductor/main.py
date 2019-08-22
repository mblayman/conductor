import os
import sys

import django
from gunicorn.app import wsgiapp

from conductor import celery


def main() -> None:
    run_func = None
    if len(sys.argv) > 1:
        run_func = COMMANDS.get(sys.argv[1])

    if run_func:
        run_func(sys.argv)
    else:
        run_gunicorn(sys.argv)


def run_celery(argv: list) -> None:
    """Run Celery."""
    celery.app.worker_main(argv[1:])


def run_manage(argv: list) -> None:
    """Run Django's manage command."""
    from django.core.management import execute_from_command_line

    execute_from_command_line(argv[1:])


def run_gunicorn(argv: list) -> None:
    """Run the web server."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
    django.setup()

    argv.append("conductor.wsgi:application")
    wsgiapp.run()


COMMANDS = {"celery": run_celery, "manage": run_manage}
