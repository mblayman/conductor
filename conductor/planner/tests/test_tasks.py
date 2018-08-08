import datetime

from django.conf import settings
from django.core import mail
from django.utils import timezone

from conductor.planner import tasks
from conductor.planner.models import Audit
from conductor.tests import TestCase


class TestAuditSchool(TestCase):

    def test_creates_audit(self):
        school = self.SchoolFactory.create()
        self.AuditFactory.create()  # Ensure filtering on a school is used.

        tasks.audit_school(school.id)

        Audit.objects.get(school=school)

    def test_skips_create_with_recent_audit(self):
        school = self.SchoolFactory.create()
        self.AuditFactory.create(school=school)

        tasks.audit_school(school.id)

        self.assertEqual(1, Audit.objects.count())

    def test_creates_audit_with_old_audit(self):
        school = self.SchoolFactory.create()
        audit = self.AuditFactory.create(school=school)
        audit.created_date = timezone.now() - datetime.timedelta(days=91)
        audit.save()

        tasks.audit_school(school.id)

        self.assertEqual(2, Audit.objects.count())

    def test_emails_admin(self):
        school = self.SchoolFactory.create()

        tasks.audit_school(school.id)

        self.assertIn(school.name, mail.outbox[0].subject)
        self.assertEqual([settings.CONDUCTOR_EMAIL], mail.outbox[0].to)
