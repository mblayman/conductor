import os
from typing import Any, Dict

from celery import Celery
from celery.signals import task_failure
from django.http import HttpRequest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("conductor")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Rollbar is not configured to run Celery out of the box.
# This gets a little harder because the code should avoid clobbering
# the work done by the Rollbar Django middleware.
# Only run the setup if the worker is running.
if bool(os.environ.get("CELERY_WORKER_RUNNING", False)):
    from django.conf import settings
    import rollbar

    rollbar.init(**settings.ROLLBAR)

    def celery_base_data_hook(request: HttpRequest, data: Dict[str, str]) -> None:
        data["framework"] = "celery"

    rollbar.BASE_DATA_HOOK = celery_base_data_hook

    @task_failure.connect
    def handle_task_failure(**kw: Any) -> None:
        rollbar.report_exc_info(extra_data=kw)
