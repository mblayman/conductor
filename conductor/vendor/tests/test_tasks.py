import os
from unittest import mock

from django.core import mail

from conductor.tests import TestCase
from conductor.vendor import tasks
from conductor.vendor.models import PromptSchool


@mock.patch("conductor.vendor.tasks.requests")
class TestScanPrompt(TestCase):
    def test_creates_prompt_school(self, mock_requests: mock.MagicMock) -> None:
        """A prompt school is found on the page and created."""
        prompt_results_path = os.path.join(
            os.path.dirname(__file__), "data", "prompt_results.html"
        )
        with open(prompt_results_path, "r") as f:
            prompt_results = f.read()
        response = mock.MagicMock()
        response.text = prompt_results
        mock_requests.get.return_value = response

        tasks.scan_prompt()

        self.assertEqual(
            1,
            PromptSchool.objects.filter(
                slug="colorado-state", name="Colorado State University"
            ).count(),
        )
        self.assertEqual(1, len(mail.outbox))
        self.assertIn("Prompt", mail.outbox[0].subject)

    def test_skip_existing_prompt_school(self, mock_requests: mock.MagicMock) -> None:
        """Skip creating a prompt school if one already exists."""
        slug = "colorado-state"
        self.PromptSchoolFactory.create(slug="colorado-state")
        prompt_results_path = os.path.join(
            os.path.dirname(__file__), "data", "prompt_results.html"
        )
        with open(prompt_results_path, "r") as f:
            prompt_results = f.read()
        response = mock.MagicMock()
        response.text = prompt_results
        mock_requests.get.return_value = response

        tasks.scan_prompt()

        self.assertEqual(1, PromptSchool.objects.filter(slug=slug).count())
