from typing import Dict
from unittest import mock

from conductor.accounts.forms import DeactivateForm, SignupForm
from conductor.tests import TestCase


class TestSignupForm(TestCase):
    def test_valid(self) -> None:
        product_plan = self.ProductPlanFactory.create()
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(product_plan, data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(product_plan, form.product_plan)

    def test_required(self) -> None:
        product_plan = self.ProductPlanFactory.create()
        data: Dict[str, str] = {}
        form = SignupForm(product_plan, data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("password", form.errors)
        self.assertIn("stripe_token", form.errors)
        self.assertNotIn("postal_code", form.errors)

    def test_invalid_password(self) -> None:
        product_plan = self.ProductPlanFactory.create()
        # Test similar username and password to ensure a user instance
        # is present and valuable.
        data = {
            "username": "mattlayman",
            "email": "matt@test.com",
            "password": "mattlayman",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(product_plan, data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_unique_email(self) -> None:
        product_plan = self.ProductPlanFactory.create()
        self.UserFactory.create(email="matt@test.com")
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(product_plan, data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_unique_username(self) -> None:
        product_plan = self.ProductPlanFactory.create()
        self.UserFactory.create(username="matt")
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "12345",
        }
        form = SignupForm(product_plan, data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    @mock.patch("conductor.accounts.forms.stripe_gateway")
    def test_creates_user(self, stripe_gateway: mock.MagicMock) -> None:
        product_plan = self.ProductPlanFactory.create()
        stripe_gateway.create_customer.return_value = "cus_1234"
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": "21702",
        }
        form = SignupForm(product_plan, data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.username, "matt")
        self.assertEqual(user.email, "matt@test.com")
        self.assertEqual(user.profile.postal_code, "21702")
        self.assertEqual(user.profile.stripe_customer_id, "cus_1234")

    @mock.patch("conductor.accounts.forms.stripe_gateway")
    def test_missing_postal_code(self, stripe_gateway: mock.MagicMock) -> None:
        product_plan = self.ProductPlanFactory.create()
        stripe_gateway.create_customer.return_value = "cus_1234"
        data = {
            "username": "matt",
            "email": "matt@test.com",
            "password": "asecrettoeverybody",
            "stripe_token": "tok_1234",
            "postal_code": None,
        }
        form = SignupForm(product_plan, data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.profile.postal_code, "")


class TestDeactivateForm(TestCase):
    def test_matching_email(self) -> None:
        user = self.UserFactory.create()
        data = {"email": user.email}
        form = DeactivateForm(user, data=data)

        is_valid = form.is_valid()

        self.assertTrue(is_valid)

    def test_mismatched_email(self) -> None:
        user = self.UserFactory.create()
        data = {"email": f"nomatch-{user.email}"}
        form = DeactivateForm(user, data=data)

        is_valid = form.is_valid()

        self.assertFalse(is_valid)
        self.assertIn("email", form.errors)
