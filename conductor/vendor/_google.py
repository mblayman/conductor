from typing import Dict

from apiclient import discovery
from google.oauth2.credentials import Credentials

from conductor.planner.models import Student

SCHEDULE_HEADER_ROW = [
    "School",
    "Application Platform",
    "Plan",
    "Out Due Date",
    "Official Due Date",
    "App Form Status",
    "Essay List (words)",
    "Essay Status",
    "Recs (req/allowed)",
    "Rec Status",
    "Transcript/School Report",
    "Transcript Status",
    "Test Scores",
    "Test Scores Status",
]


class GoogleGateway:
    """A gateway to Google products"""

    def __init__(self, credentials: Credentials) -> None:
        self.credentials = credentials

    def generate_schedule(self, student: Student) -> None:
        """Generate the schedule of schools for a student.

        The data is exported to the user's Google Drive.
        """
        sheets_client = discovery.build(
            "sheets", "v4", credentials=self.credentials, cache_discovery=False
        )
        data = {
            "properties": {"title": "{} - Application Status".format(student)},
            "sheets": [
                {
                    "properties": {
                        "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 1}
                    },
                    "data": [
                        {
                            "startRow": 0,
                            "startColumn": 0,
                            "rowData": [self.build_header_row()],
                        }
                    ],
                }
            ],
        }
        sheets_client.spreadsheets().create(body=data).execute()

    def build_header_row(self) -> Dict:
        """Build the header row of cells."""
        return {
            "values": [
                {"userEnteredValue": {"stringValue": column_name}}
                for column_name in SCHEDULE_HEADER_ROW
            ]
        }
