from typing import Dict
from unittest import mock

from conductor.accounts.forms import SignupForm
from conductor.tests import TestCase


class TestSignupForm(TestCase):
    def test_valid(self):
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(data)

        self.assertTrue(form.is_valid())

    def test_required(self):
        data: Dict[str, str] = {}
        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("password", form.errors)
        self.assertIn("stripe_token", form.errors)
        self.assertNotIn("postal_code", form.errors)

    def test_invalid_password(self):
        # Test similar username and password to ensure a user instance
        # is present and valuable.
        data = {
            "username": "mattlayman",
            "email": "matt@test.com",
            "password": "mattlayman",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_unique_email(self):
        self.UserFactory.create(email="matt@test.com")
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_unique_username(self):
        self.UserFactory.create(username="matt")
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    @mock.patch("conductor.accounts.forms.stripe_gateway")
    def test_creates_user(self, stripe_gateway):
        stripe_gateway.create_customer.return_value = "cus_1234"
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "21702",
        }
        form = SignupForm(data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.username, "matt")
        self.assertEqual(user.email, "matt@test.com")
        self.assertEqual(user.profile.postal_code, "21702")
        self.assertEqual(user.profile.stripe_customer_id, "cus_1234")

    @mock.patch("conductor.accounts.forms.stripe_gateway")
    def test_missing_postal_code(self, stripe_gateway):
        stripe_gateway.create_customer.return_value = "cus_1234"
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": None,
        }
        form = SignupForm(data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.profile.postal_code, "")
