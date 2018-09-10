import datetime
from unittest import mock

from django.conf import settings
from django.core import mail
from django.utils import timezone
from google.oauth2.credentials import Credentials

from conductor.planner import tasks
from conductor.planner.models import Audit
from conductor.tests import TestCase


class TestAuditSchool(TestCase):
    def test_creates_audit(self) -> None:
        school = self.SchoolFactory.create()
        semester = self.SemesterFactory.create()
        self.AuditFactory.create()  # Ensure filtering on a school is used.

        tasks.audit_school(school.id, semester.id)

        Audit.objects.get(school=school)

    def test_skips_create_with_recent_audit(self) -> None:
        school = self.SchoolFactory.create()
        semester = self.SemesterFactory.create()
        self.AuditFactory.create(school=school, semester=semester)

        tasks.audit_school(school.id, semester.id)

        self.assertEqual(1, Audit.objects.count())

    def test_creates_audit_with_old_audit(self) -> None:
        school = self.SchoolFactory.create()
        semester = self.SemesterFactory.create()
        audit = self.AuditFactory.create(school=school, semester=semester)
        audit.created_date = timezone.now() - datetime.timedelta(days=91)
        audit.save()

        tasks.audit_school(school.id, semester.id)

        self.assertEqual(2, Audit.objects.count())

    def test_emails_admin(self) -> None:
        school = self.SchoolFactory.create()
        semester = self.SemesterFactory.create()

        tasks.audit_school(school.id, semester.id)

        self.assertIn(school.name, mail.outbox[0].subject)
        self.assertIn(str(semester), mail.outbox[0].subject)
        self.assertEqual([settings.CONDUCTOR_EMAIL], mail.outbox[0].to)


@mock.patch("conductor.planner.tasks.GoogleGateway")
class TestBuildSchedule(TestCase):
    def test_creates_google_sheet(self, GoogleGateway: mock.MagicMock) -> None:
        gateway_instance = mock.Mock()
        GoogleGateway.return_value = gateway_instance
        student = self.StudentFactory.create()
        self.GoogleDriveAuthFactory.create(user=student.user)

        tasks.build_schedule(student.id)

        gateway_instance.generate_schedule.assert_called_once_with(student)

    def test_updates_refresh_token(self, GoogleGateway: mock.MagicMock) -> None:
        """A refresh token is updated when credentials change.

        Google can update the refresh token as a side effect of the auth process.
        The persisted refresh token is updated to reflect this change.
        """
        gateway_instance = mock.Mock()

        def change_refresh_token(credentials: Credentials) -> mock.Mock:
            credentials._refresh_token = "a new token"
            return gateway_instance

        # credentials would actually change from generate_schedule.
        # This is close enough.
        GoogleGateway.side_effect = change_refresh_token
        GoogleGateway.return_value = gateway_instance
        student = self.StudentFactory.create()
        auth = self.GoogleDriveAuthFactory.create(user=student.user)

        tasks.build_schedule(student.id)

        auth.refresh_from_db()
        self.assertEqual("a new token", auth.refresh_token)

    def test_creates_application_schedule(self, GoogleGateway: mock.MagicMock) -> None:
        """A record of the generation is stored."""
        student = self.StudentFactory.create()
        self.GoogleDriveAuthFactory.create(user=student.user)

        tasks.build_schedule(student.id)

        self.assertEqual(1, student.schedules.count())
