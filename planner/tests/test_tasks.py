import datetime

from django.utils import timezone

from conductor.tests import TestCase
from planner import tasks
from planner.models import Audit


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
