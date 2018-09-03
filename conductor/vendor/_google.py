from collections import namedtuple
from typing import Dict

from apiclient import discovery
from google.oauth2.credentials import Credentials

from conductor.planner.models import Student

GoogleSpreadsheet = namedtuple("GoogleSpreadsheet", ["spreadsheet_id", "sheet_id"])

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
        service = discovery.build(
            "sheets", "v4", credentials=self.credentials, cache_discovery=False
        )
        spreadsheets_resource = service.spreadsheets()

        google_spreadsheet = self.create_sheet(student, spreadsheets_resource)
        self.format_sheet(google_spreadsheet, spreadsheets_resource)

    def create_sheet(
        self, student: Student, spreadsheets_resource: discovery.Resource
    ) -> GoogleSpreadsheet:
        """Add the raw data to the sheet."""
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
        response = spreadsheets_resource.create(body=data).execute()
        return GoogleSpreadsheet(
            response["spreadsheetId"], response["sheets"][0]["properties"]["sheetId"]
        )

    def build_header_row(self) -> Dict:
        """Build the header row of cells."""
        return {
            "values": [
                {"userEnteredValue": {"stringValue": column_name}}
                for column_name in SCHEDULE_HEADER_ROW
            ]
        }

    def format_sheet(
        self,
        google_spreadsheet: GoogleSpreadsheet,
        spreadsheets_resource: discovery.Resource,
    ) -> None:
        """Format the newly created sheet.

        The create API isn't designed to work with ranges so this method sets
        the formatting of the newly created sheet.
        """
        data = {
            "requests": [
                # Set default font.
                {
                    "repeatCell": {
                        "range": {"sheetId": google_spreadsheet.sheet_id},
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {
                                    "fontFamily": "Merriweather",
                                    "fontSize": 10,
                                }
                            }
                        },
                        "fields": "userEnteredFormat.textFormat",
                    }
                },
                # Update header row font properties.
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": google_spreadsheet.sheet_id,
                            "endRowIndex": 1,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {
                                    "fontSize": 12,
                                    "bold": True,
                                    "underline": True,
                                }
                            }
                        },
                        "fields": "userEnteredFormat.textFormat(fontSize,bold,underline)",  # noqa
                    }
                },
            ]
        }
        spreadsheets_resource.batchUpdate(
            spreadsheetId=google_spreadsheet.spreadsheet_id, body=data
        ).execute()
