from typing import Dict
from unittest import mock

from django.urls import reverse

from conductor.support import views
from conductor.support.models import SupportTicket
from conductor.tests import TestCase


class TestContact(TestCase):
    def test_get(self):
        request = self.request_factory.get()

        response = views.contact(request)

        self.assertEqual(200, response.status_code)

    @mock.patch("conductor.support.views.render")
    def test_has_form(self, render):
        request = self.request_factory.get()

        views.contact(request)

        context = render.call_args[0][2]
        self.assertIn("form", context)

    @mock.patch("conductor.support.views.messages")
    def test_success(self, messages):
        data = {
            "email": "matt@test.com",
            "subject": "Help me",
            "message": "I need your help.",
        }
        request = self.request_factory.post(data=data)

        response = views.contact(request)

        self.assertEqual(1, SupportTicket.objects.count())
        self.assertIn(reverse("contact"), response.get("Location"))
        messages.add_message.assert_called_once_with(
            request, messages.SUCCESS, mock.ANY
        )

    @mock.patch("conductor.support.views.render")
    def test_failure(self, render):
        data: Dict[str, str] = {}
        request = self.request_factory.post(data=data)

        views.contact(request)

        context = render.call_args[0][2]
        self.assertFalse(context["form"].is_valid())
