from collections import namedtuple
from typing import Dict, List

from apiclient import discovery
from django.db.models import Prefetch, QuerySet
from google.oauth2.credentials import Credentials

from conductor.planner.models import Milestone, Student, TargetSchool

GoogleSpreadsheet = namedtuple(
    "GoogleSpreadsheet", ["spreadsheet_id", "sheet_id", "schools_count"]
)

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
SCHOOL_GROUP_SIZE = 7


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
        target_schools = TargetSchool.objects.filter(student=student)
        target_schools = target_schools.select_related("school")
        prefetch = Prefetch(
            "milestones", queryset=Milestone.objects.all().order_by("date")
        )
        target_schools = target_schools.prefetch_related(prefetch)
        target_schools = target_schools.order_by("school__name")

        row_data = [self.build_header_row()]
        row_data.extend(self.build_school_rows(target_schools))

        data = {
            "properties": {"title": "{} - Application Status".format(student)},
            "sheets": [
                {
                    "properties": {
                        "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 1}
                    },
                    "data": [{"startRow": 0, "startColumn": 0, "rowData": row_data}],
                }
            ],
        }
        response = spreadsheets_resource.create(body=data).execute()
        return GoogleSpreadsheet(
            response["spreadsheetId"],
            response["sheets"][0]["properties"]["sheetId"],
            target_schools.count(),
        )

    def build_header_row(self) -> Dict:
        """Build the header row of cells."""
        return {
            "values": [
                {"userEnteredValue": {"stringValue": column_name}}
                for column_name in SCHEDULE_HEADER_ROW
            ]
        }

    def build_school_rows(self, target_schools: QuerySet) -> List:
        """Build the rows for each school."""
        school_rows = []
        for target_school in target_schools:
            school_rows.append(
                {
                    "values": [
                        {"userEnteredValue": {"stringValue": target_school.school.name}}
                    ]
                }
            )
            remaining_rows = SCHOOL_GROUP_SIZE - 1

            # Fill with each selected milestone.
            for milestone in target_school.milestones.all():
                school_rows.append(
                    {
                        "values": [
                            {},
                            {},
                            {"userEnteredValue": {"stringValue": milestone.category}},
                            {
                                "userEnteredValue": {
                                    "stringValue": "{:%B %-d}".format(milestone.date)
                                }
                            },
                        ]
                    }
                )
                remaining_rows -= 1

            # Pad remaining slots.
            for _ in range(remaining_rows):
                school_rows.append(self.build_empty_row())

        return school_rows

    def build_empty_row(self) -> Dict[str, List]:
        """Build an empty row."""
        return {"values": []}

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

        # Border rows between school groups.
        # Shift by 1 on the range to get the math right.
        for i in range(1, google_spreadsheet.schools_count + 1):
            # It seems like this should add 1 to account for the header row,
            # but rows are zero indexed so leaving off an increment
            # does the right thing.
            row_index = i * SCHOOL_GROUP_SIZE
            data["requests"].append(self.border_row_bottom(row_index, sheet_id))

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
                "fields": "userEnteredFormat.borders.right.style",
            }
        }

    def border_row_bottom(self, row_index: int, sheet_id: int) -> Dict:
        """Border the right side of a row."""
        return {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_index,
                    "endRowIndex": row_index + 1,
                },
                "cell": {
                    "userEnteredFormat": {
                        "borders": {"bottom": {"style": "SOLID_MEDIUM"}}
                    }
                },
                "fields": "userEnteredFormat.borders.bottom.style",
            }
        }
