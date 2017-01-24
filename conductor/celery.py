import os

from celery import Celery
from celery.signals import task_failure

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'conductor.settings.development')

app = Celery('conductor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Rollbar is not configured to run Celery out of the box.
# This gets a little harder because the code should avoid clobbering
# the work done by the Rollbar Django middleware.
# Only run the setup if the worker is running.
if bool(os.environ.get('CELERY_WORKER_RUNNING', False)):
    from django.conf import settings
    import rollbar
    rollbar.init(**settings.ROLLBAR)

    def celery_base_data_hook(request, data):
        data['framework'] = 'celery'

    rollbar.BASE_DATA_HOOK = celery_base_data_hook

    @task_failure.connect
    def handle_task_failure(**kw):
        rollbar.report_exc_info(extra_data=kw)
