from apiclient import discovery
from google.oauth2.credentials import Credentials

from conductor.planner.models import Student


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
        data = {"properties": {"title": "{} - Application Status".format(student)}}
        sheets_client.spreadsheets().create(body=data).execute()
