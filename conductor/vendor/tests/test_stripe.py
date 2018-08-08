from unittest import mock

from conductor.tests import TestCase
from conductor.vendor._stripe import StripeGateway


class TestStripeGateway(TestCase):

    @mock.patch('conductor.vendor._stripe.stripe')
    def test_create_customer(self, stripe):
        customer = mock.Mock()
        customer.id = 'cus_1234'
        stripe.Customer.create.return_value = customer
        user = self.UserFactory.create()
        stripe_token = 'tok_1234'
        stripe_gateway = StripeGateway()

        stripe_customer_id = stripe_gateway.create_customer(user, stripe_token)

        self.assertEqual(stripe_customer_id, 'cus_1234')

    @mock.patch('conductor.vendor._stripe.stripe')
    def test_bad_token(self, stripe):
        """For now, let Stripe errors go. Catch them in Rollbar."""
        class InvalidRequestError(Exception):
            pass

        stripe.Customer.create.side_effect = InvalidRequestError
        user = self.UserFactory.create()
        stripe_token = 'tok_invalid'
        stripe_gateway = StripeGateway()

        with self.assertRaises(InvalidRequestError):
            stripe_gateway.create_customer(user, stripe_token)
