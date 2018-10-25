from unittest import mock

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

        handler.process_school(raw_school)

        self.assertTrue(CommonAppTracker.objects.filter(slug="uva").exists())

    def test_modifies_tracker(self) -> None:
        """A raw school that already exists updates the school name."""
        raw_school = RawCommonAppSchool(name="UVA", slug="uva")
        self.CommonAppTrackerFactory.create(
            name="University of Virginia", slug=raw_school.slug
        )
        handler = CommonAppHandler()

        handler.process_school(raw_school)

        common_app_tracker = CommonAppTracker.objects.get(slug=raw_school.slug)
        self.assertEqual(raw_school.name, common_app_tracker.name)
