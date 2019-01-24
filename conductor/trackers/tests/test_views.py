from unittest import mock

from django.urls import reverse

from conductor.tests import TestCase
from conductor.trackers import views
from conductor.trackers.models import CommonAppTracker


class TestConnectCommonApps(TestCase):
    def test_staff_only(self) -> None:
        user = self.UserFactory.create(is_staff=False)
        request = self.request_factory.authenticated_get(user)

        response = views.connect_common_apps(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_ok(self) -> None:
        user = self.UserFactory.create(is_staff=True)
        request = self.request_factory.authenticated_get(user)

        response = views.connect_common_apps(request)

        self.assertEqual(200, response.status_code)

    @mock.patch("conductor.trackers.views.render")
    def test_context(self, render: mock.MagicMock) -> None:
        common_app_tracker = self.CommonAppTrackerFactory.create(
            status=CommonAppTracker.PENDING
        )
        self.CommonAppTrackerFactory.create(status=CommonAppTracker.TRACKED)
        user = self.UserFactory.create(is_staff=True)
        request = self.request_factory.authenticated_get(user)

        views.connect_common_apps(request)

        context = render.call_args[0][2]
        self.assertEqual(common_app_tracker, context["common_app_tracker"])

    @mock.patch("conductor.trackers.views.render")
    def test_find_matching_school(self, render: mock.MagicMock) -> None:
        name = "University of Virginia"
        self.CommonAppTrackerFactory.create(name=name, status=CommonAppTracker.PENDING)
        school = self.SchoolFactory.create(name=name)
        self.SchoolFactory.create(name="Johns Hopkins University")
        user = self.UserFactory.create(is_staff=True)
        request = self.request_factory.authenticated_get(user)

        views.connect_common_apps(request)

        context = render.call_args[0][2]
        self.assertEqual(1, len(context["schools"]))
        self.assertEqual(school, context["schools"][0])
