import os
from unittest import mock

from conductor.tests import TestCase

from conductor.trackers import tasks


@mock.patch("conductor.trackers.tasks.common_app_handler")
@mock.patch("conductor.trackers.tasks.time")
@mock.patch("conductor.trackers.tasks.requests")
class TestScanCommonAppSchools(TestCase):
    def test_scan(
        self,
        mock_requests: mock.MagicMock,
        mock_time: mock.MagicMock,
        common_app_handler: mock.MagicMock,
    ) -> None:
        common_app_results_path = os.path.join(
            os.path.dirname(__file__), "data", "common_app_results.html"
        )
        with open(common_app_results_path, "r") as f:
            common_app_results = f.read()
        response = mock.MagicMock()
        response.text = common_app_results
        empty_response = mock.MagicMock()
        empty_response.text = ""
        mock_requests.get.side_effect = [response, empty_response]

        tasks.scan_common_app_schools()

        self.assertTrue(common_app_handler.handle.called)
        call_args = common_app_handler.handle.call_args
        self.assertEqual(1, len(call_args[0][0]))
