import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conductor.settings.development')

app = Celery('conductor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
