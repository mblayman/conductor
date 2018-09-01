from apiclient import discovery
from django.utils import timezone
from google.oauth2.credentials import Credentials

from conductor.planner.models import Student


class GoogleGateway:
    """A gateway to Google products"""

    def __init__(self, credentials: Credentials) -> None:
        self.credentials = credentials

    def generate_schedule(self, student: Student) -> None:
        sheets_client = discovery.build(
            "sheets", "v4", credentials=self.credentials, cache_discovery=False
        )
        data = {
            "properties": {"title": "Sample spreadsheet from {}".format(timezone.now())}
        }
        sheets_client.spreadsheets().create(body=data).execute()
