from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from conductor.core.decorators import staff_required
from conductor.tests import TestCase


@staff_required
def staff_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("")


class TestStaffRequired(TestCase):
    def test_anonymous(self) -> None:
        request = self.request_factory.get()

        response = staff_view(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_redirect_non_staff(self) -> None:
        user = self.UserFactory.create(is_staff=False)
        request = self.request_factory.authenticated_get(user)

        response = staff_view(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_allow_staff_only(self) -> None:
        user = self.UserFactory.create(is_staff=True)
        request = self.request_factory.authenticated_get(user)

        response = staff_view(request)

        self.assertEqual(200, response.status_code)
