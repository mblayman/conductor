from unittest import mock

from conductor.tests import TestCase
from conductor.vendor._google import GoogleGateway


@mock.patch("conductor.vendor._google.discovery")
class TestGoogleGateway(TestCase):
    def setup_mock_for_sheets(self, mock_discovery):
        """Set up the mocks to pretend to be the discovery API.

        This is a maze.
        """
        self.spreadsheets = mock.Mock()
        sheets_client = mock.Mock()
        sheets_client.spreadsheets.return_value = self.spreadsheets
        mock_discovery.build.return_value = sheets_client

    def get_create_data(self):
        """Get the data sent to create out of the mock."""
        return self.spreadsheets.create.call_args_list[0][1]["body"]

    def test_sheet_title(self, mock_discovery) -> None:
        """Title contains the student name."""
        self.setup_mock_for_sheets(mock_discovery)
        student = self.StudentFactory.create()
        credentials = mock.Mock()
        gateway = GoogleGateway(credentials)

        gateway.generate_schedule(student)

        expected_title = "{} - Application Status".format(student)
        data = self.get_create_data()
        self.assertEqual(expected_title, data["properties"]["title"])
