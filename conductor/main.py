import os

import django
from gunicorn.app import wsgiapp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
django.setup()
wsgiapp.run()
