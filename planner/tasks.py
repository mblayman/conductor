import datetime

from django.utils import timezone

from conductor import celeryapp
from planner.models import Audit


@celeryapp.task
def audit_school(school_id):
    """Audit a school if it has not been recently audited."""
    audit_window = timezone.now() - datetime.timedelta(days=90)
    if not Audit.objects.filter(
            created_date__gt=audit_window, school_id=school_id).exists():
        Audit.objects.create(school_id=school_id)
