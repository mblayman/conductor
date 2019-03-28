from unittest import mock

from conductor.core.exceptions import ConductorError
from conductor.tests import TestCase
from conductor.vendor._stripe import StripeGateway


class TestStripeGateway(TestCase):
    @mock.patch("conductor.vendor._stripe.stripe")
    def test_create_customer(self, stripe: mock.MagicMock) -> None:
        customer = mock.Mock()
        customer.id = "cus_1234"
        stripe.Customer.create.return_value = customer
        user = self.UserFactory.create()
        stripe_token = "tok_1234"
        product_plan = self.ProductPlanFactory.create()
        stripe_gateway = StripeGateway()

        stripe_customer_id = stripe_gateway.create_customer(
            user, stripe_token, product_plan
        )

        self.assertEqual(stripe_customer_id, "cus_1234")

    @mock.patch("conductor.vendor._stripe.stripe")
    def test_bad_token(self, stripe: mock.MagicMock) -> None:
        """For now, let Stripe errors go. Catch them in Rollbar."""

        class InvalidRequestError(Exception):
            pass

        stripe.Customer.create.side_effect = InvalidRequestError
        user = self.UserFactory.create()
        stripe_token = "tok_invalid"
        product_plan = self.ProductPlanFactory.create()
        stripe_gateway = StripeGateway()

        with self.assertRaises(InvalidRequestError):
            stripe_gateway.create_customer(user, stripe_token, product_plan)

    @mock.patch("conductor.vendor._stripe.stripe")
    def test_cancel_subscription(self, stripe: mock.MagicMock) -> None:
        """A user can cancel their subscription."""
        user = self.UserFactory.create()
        customer = mock.MagicMock()
        stripe.Customer.retrieve.return_value = customer
        subscription = mock.MagicMock()
        stripe.Subscription.retrieve.return_value = subscription
        stripe_gateway = StripeGateway()

        stripe_gateway.cancel_subscription(user)

        stripe.Customer.retrieve.assert_called_once_with(
            user.profile.stripe_customer_id
        )
        self.assertTrue(subscription.delete.called)

    @mock.patch("conductor.vendor._stripe.stripe")
    def test_cancel_subscription_error(self, stripe: mock.MagicMock) -> None:
        """A Stripe error raises a conductor error."""

        class StripeError(Exception):
            pass

        stripe.error.StripeError = StripeError
        user = self.UserFactory.create()
        stripe.Customer.retrieve.side_effect = stripe.error.StripeError
        stripe_gateway = StripeGateway()

        with self.assertRaises(ConductorError):
            stripe_gateway.cancel_subscription(user)
