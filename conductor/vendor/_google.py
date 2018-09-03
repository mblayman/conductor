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
    "Interview",
    "Interview Status",
    "Portfolio",
    "Portfolio Status",
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
        sheet_id = google_spreadsheet.sheet_id
        data = {
            "requests": [
                # Set default font.
                {
                    "repeatCell": {
                        "range": {"sheetId": sheet_id},
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {"fontFamily": "Average", "fontSize": 10}
                            }
                        },
                        "fields": "userEnteredFormat.textFormat",
                    }
                },
                # Update header row font properties.
                {
                    "repeatCell": {
                        "range": {"sheetId": sheet_id, "endRowIndex": 1},
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
                # Autoresize columns that are too narrow.
                {
                    "autoResizeDimensions": {
                        "dimensions": {"sheetId": sheet_id, "dimension": "COLUMNS"}
                    }
                },
                # Allow more space for the essay list prompts.
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "COLUMNS",
                            "startIndex": 6,
                            "endIndex": 7,
                        },
                        "properties": {"pixelSize": 314},
                        "fields": "pixelSize",
                    }
                },
                # Border columns that need borders.
                self.border_column_right(4, sheet_id),
                self.border_column_right(5, sheet_id),
                self.border_column_right(7, sheet_id),
                self.border_column_right(9, sheet_id),
                self.border_column_right(11, sheet_id),
                self.border_column_right(13, sheet_id),
                self.border_column_right(15, sheet_id),
                self.border_column_right(17, sheet_id),
            ]
        }
        spreadsheets_resource.batchUpdate(
            spreadsheetId=google_spreadsheet.spreadsheet_id, body=data
        ).execute()

    def border_column_right(self, column_index: int, sheet_id: int) -> Dict:
        """Border the right side of a column."""
        return {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": column_index,
                    "endColumnIndex": column_index + 1,
                },
                "cell": {
                    "userEnteredFormat": {"borders": {"right": {"style": "SOLID"}}}
                },
                "fields": "userEnteredFormat.borders.right.style",  # noqa
            }
        }
