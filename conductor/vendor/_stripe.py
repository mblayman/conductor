from django.conf import settings
import stripe

from conductor.accounts.models import User

stripe.api_key = settings.STRIPE_API_KEY


class StripeGateway:
    """A gateway to Stripe

    This insulates the rest of the system from Stripe errors
    and configures the Stripe module with the API key.
    """

    def create_customer(self, user: User, stripe_token: str) -> str:
        """Add a user to Stripe and join them to the plan."""
        # Let this fail on purpose. If it fails, the error monitoring system
        # will log it and I'll learn how to harden it for the conductor env.
        customer = stripe.Customer.create(
            email=user.email, plan="monthly-14d-1", source=stripe_token
        )
        return customer.id


stripe_gateway = StripeGateway()
