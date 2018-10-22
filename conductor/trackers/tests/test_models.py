from conductor.tests import TestCase
from conductor.trackers.models import CommonAppTracker


class TestCommonAppTracker(TestCase):
    def test_factory(self) -> None:
        tracker = self.CommonAppTrackerFactory.create()

        self.assertIsNotNone(tracker.created_date)
        self.assertNotEqual("", tracker.name)
        self.assertNotEqual("", tracker.slug)
        self.assertIsNone(tracker.school)

    def test_has_name(self) -> None:
        tracker = self.CommonAppTrackerFactory.create(name="University of Virginia")

        self.assertEqual("University of Virginia", tracker.name)

    def test_has_slug(self) -> None:
        tracker = self.CommonAppTrackerFactory.create(slug="university-of-virginia")

        self.assertEqual("university-of-virginia", tracker.slug)

    def test_has_status(self) -> None:
        tracker = self.CommonAppTrackerFactory.create()

        self.assertEqual(CommonAppTracker.PENDING, tracker.status)

    def test_has_school(self) -> None:
        school = self.SchoolFactory.create()
        tracker = self.CommonAppTrackerFactory.create(school=school)

        self.assertEqual(school, tracker.school)
