import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils import timezone

from conductor import celeryapp
from conductor.accounts.models import GoogleDriveAuth
from conductor.planner.models import (
    ApplicationSchedule,
    Audit,
    School,
    Semester,
    Student,
)
from conductor.vendor.services import GoogleGateway


@celeryapp.task
def audit_school(school_id: int, semester_id: int) -> None:
    """Audit a school if it has not been recently audited."""
    audit_window = timezone.now() - datetime.timedelta(days=90)
    if not Audit.objects.filter(
        created_date__gt=audit_window, school_id=school_id, semester_id=semester_id
    ).exists():
        Audit.objects.create(school_id=school_id, semester_id=semester_id)
        school = School.objects.get(id=school_id)
        semester = Semester.objects.get(id=semester_id)
        school_url = "{}{}".format(
            settings.DOMAIN, reverse("admin:planner_school_change", args=[school_id])
        )
        email = EmailMessage(
            f"An audit of {school.name} is required for {semester}",
            f"Time to make the donuts\n\n{school_url}",
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
