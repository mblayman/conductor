from typing import Dict, List
from unittest import mock

from django.core import mail

from conductor.tests import TestCase
from conductor.trackers.handlers import CommonAppHandler
from conductor.trackers.models import CommonAppTracker, RawCommonAppSchool


class TestCommonAppHandler(TestCase):
    @mock.patch.object(CommonAppHandler, "process_school")
    def test_no_action_when_all_tracked(self, process_school: mock.MagicMock) -> None:
        self.CommonAppTrackerFactory.create(status=CommonAppTracker.REMOVED)
        self.CommonAppTrackerFactory.create()
        common_app_schools = [RawCommonAppSchool(name="UVA", slug="uva")]
        handler = CommonAppHandler()

        handler.handle(common_app_schools)

        self.assertFalse(process_school.called)

    def test_add_tracker(self) -> None:
        """A raw school is added as a tracker if missing."""
        raw_school = RawCommonAppSchool(name="UVA", slug="uva")
        handler = CommonAppHandler()
        stats: Dict[str, List[CommonAppTracker]] = {"add": []}

        handler.process_school(raw_school, stats)

        common_app_tracker = CommonAppTracker.objects.get(slug="uva")
        self.assertEqual([common_app_tracker], stats["add"])

    def test_modifies_tracker(self) -> None:
        """A raw school that already exists updates the school name."""
        raw_school = RawCommonAppSchool(name="UVA", slug="uva")
        self.CommonAppTrackerFactory.create(
            name="University of Virginia", slug=raw_school.slug
        )
        handler = CommonAppHandler()
        stats: Dict[str, List[CommonAppTracker]] = {"modify": []}

        handler.process_school(raw_school, stats)

        common_app_tracker = CommonAppTracker.objects.get(slug=raw_school.slug)
        self.assertEqual(raw_school.name, common_app_tracker.name)
        self.assertEqual([common_app_tracker], stats["modify"])

    def test_same_school_name(self) -> None:
        """A school with the same name is not modified."""
        raw_school = RawCommonAppSchool(name="UVA", slug="uva")
        self.CommonAppTrackerFactory.create(name=raw_school.name, slug=raw_school.slug)
        handler = CommonAppHandler()
        stats: Dict[str, List[CommonAppTracker]] = {"modify": []}

        handler.process_school(raw_school, stats)

        self.assertEqual(0, len(stats["modify"]))

    @mock.patch.object(CommonAppHandler, "report")
    def test_tracker_removed(self, report: mock.MagicMock) -> None:
        """A tracker that no longer appears in the raw data is marked removed."""
        common_app_tracker = self.CommonAppTrackerFactory.create()
        common_app_schools: List[RawCommonAppSchool] = []
        handler = CommonAppHandler()

        handler.handle(common_app_schools)

        stats = report.call_args[0][0]
        self.assertEqual([common_app_tracker], stats["delete"])

    def test_report(self) -> None:
        """The email report is sent."""
        added_tracker = self.CommonAppTrackerFactory.create()
        modified_tracker = self.CommonAppTrackerFactory.create()
        deleted_tracker = self.CommonAppTrackerFactory.create()
        stats = {
            "add": [added_tracker],
            "modify": [modified_tracker],
            "delete": [deleted_tracker],
        }
        handler = CommonAppHandler()

        handler.report(stats)

        expected_body = f"""Add:
{added_tracker.name}

Modify:
{modified_tracker.name}

Delete:
{deleted_tracker.name}"""
        self.assertEqual(1, len(mail.outbox))
        email_message = mail.outbox[0]
        self.assertEqual("Common App Schools Processed", email_message.subject)
        self.assertEqual(expected_body, email_message.body)
