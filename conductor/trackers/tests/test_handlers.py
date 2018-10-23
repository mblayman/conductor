from unittest import mock

from conductor.tests import TestCase
from conductor.trackers.handlers import CommonAppHandler
from conductor.trackers.models import RawCommonAppSchool


class TestCommonAppHandler(TestCase):
    @mock.patch.object(CommonAppHandler, "process_school")
    def test_no_action_when_all_tracked(self, process_school: mock.MagicMock) -> None:
        self.CommonAppTrackerFactory.create()
        common_app_schools = [RawCommonAppSchool(name="UVA", slug="uva")]
        handler = CommonAppHandler()

        handler.handle(common_app_schools)

        self.assertFalse(process_school.called)
