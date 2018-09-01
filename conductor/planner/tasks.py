import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from conductor import celeryapp
from conductor.accounts.models import GoogleDriveAuth
from conductor.planner.models import ApplicationSchedule, Audit, School, Student
from conductor.vendor.services import GoogleGateway


@celeryapp.task
def audit_school(school_id: int) -> None:
    """Audit a school if it has not been recently audited."""
    audit_window = timezone.now() - datetime.timedelta(days=90)
    if not Audit.objects.filter(
        created_date__gt=audit_window, school_id=school_id
    ).exists():
        Audit.objects.create(school_id=school_id)
        school = School.objects.get(id=school_id)
        email = EmailMessage(
            u"An audit of {} is required".format(school.name),
            u"Time to make the donuts",
            to=[settings.CONDUCTOR_EMAIL],
        )
        email.send()


@celeryapp.task
def build_schedule(student_id: int) -> None:
    """Build a schedule and export it to Google Sheets."""
    student = Student.objects.get(id=student_id)

    auth = GoogleDriveAuth.objects.get(user=student.user_id)
    credentials = auth.credentials
    google_gateway = GoogleGateway(credentials)
    google_gateway.generate_schedule(student)
    ApplicationSchedule.objects.create(student=student)

    # Update the refresh token in case it changed.
    auth.refresh_token = credentials.refresh_token
    auth.save()
