from unittest import mock

from django.conf import settings
from django.urls import reverse

from conductor.accounts import views
from conductor.accounts.models import GoogleDriveAuth
from conductor.tests import TestCase


class TestSignup(TestCase):
    @mock.patch("conductor.accounts.views.render")
    def test_stripe_publishable_key_in_context(self, render):
        request = self.request_factory.get()

        views.signup(request)

        context = render.call_args[0][2]
        self.assertEqual(
            settings.STRIPE_PUBLISHABLE_KEY, context["stripe_publishable_key"]
        )

    @mock.patch("conductor.accounts.forms.stripe_gateway")
    def test_success(self, stripe_gateway):
        stripe_gateway.create_customer.return_value = "cus_1234"
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        request = self.request_factory.post(data=data, format="multipart", session=True)

        response = views.signup(request)

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(response.content.decode("utf-8"), {"status": "success"})

    def test_failure(self):
        data = {
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        request = self.request_factory.post(data=data)

        response = views.signup(request)

        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"status": "error", "errors": {"username": ["This field is required."]}},
        )


class TestDashboard(TestCase):
    def test_requires_login(self):
        request = self.request_factory.get()

        response = views.dashboard(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_get(self):
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user)

        response = views.dashboard(request)

        self.assertEqual(200, response.status_code)

    @mock.patch("conductor.accounts.views.render")
    def test_app_nav(self, render):
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user)

        views.dashboard(request)

        context = render.call_args[0][2]
        self.assertEqual("dashboard", context["app_nav"])

    @mock.patch("conductor.accounts.views.render")
    def test_students_in_context(self, render):
        user = self.UserFactory.create()
        student = self.StudentFactory.create(user=user)
        request = self.request_factory.authenticated_get(user)

        views.dashboard(request)

        context = render.call_args[0][2]
        self.assertEqual([student], list(context["students"]))


class TestUserSettings(TestCase):
    def test_requires_login(self):
        request = self.request_factory.get()

        response = views.user_settings(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_get(self):
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user)

        response = views.user_settings(request)

        self.assertEqual(200, response.status_code)

    @mock.patch("conductor.accounts.views.render")
    def test_app_nav(self, render):
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user)

        views.user_settings(request)

        context = render.call_args[0][2]
        self.assertEqual("settings", context["app_nav"])


class TestAuthorizeGoogle(TestCase):
    def test_requires_login(self):
        request = self.request_factory.get()

        response = views.authorize_google(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_get(self):
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user, session=True)

        response = views.authorize_google(request)

        self.assertEqual(302, response.status_code)
        # The authorization URL has a scope in it so look for something
        # that is part of the scope URL.
        self.assertIn("googleapis", response.get("Location"))
        self.assertNotEqual("", request.session["state"])


class TestOauth2Callback(TestCase):
    def test_requires_login(self):
        request = self.request_factory.get()

        response = views.oauth2_callback(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    @mock.patch("conductor.accounts.views.Flow")
    def test_get(self, Flow):
        credentials = mock.Mock()
        credentials.token = "fake_token"
        credentials.refresh_token = "fake_refresh_token"
        credentials.id_token = "fake_id_token"
        flow = mock.Mock()
        flow.credentials = credentials
        Flow.from_client_config.return_value = flow
        user = self.UserFactory.create()
        request = self.request_factory.authenticated_get(user, session=True)

        response = views.oauth2_callback(request)

        auth = GoogleDriveAuth.objects.get(user=user)
        self.assertEqual("fake_token", auth.token)
        self.assertEqual("fake_refresh_token", auth.refresh_token)
        self.assertEqual("fake_id_token", auth.id_token)
        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("settings"), response.get("Location"))

    @mock.patch("conductor.accounts.views.messages")
    def test_error(self, messages):
        user = self.UserFactory.create()
        data = {"error": "access_denied"}
        request = self.request_factory.authenticated_get(user, data=data, session=True)

        response = views.oauth2_callback(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("settings"), response.get("Location"))
        messages.add_message.assert_called_once_with(request, messages.ERROR, mock.ANY)
