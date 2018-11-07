from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_API_KEY
stripe.api_version = "2018-10-31"


class StripeGateway:
    """A gateway to Stripe

    This insulates the rest of the system from Stripe errors
    and configures the Stripe module with the API key.
    """

    def create_customer(self, user: settings.AUTH_USER_MODEL, stripe_token: str) -> str:
        """Add a user to Stripe and join them to the plan."""
        # Let this fail on purpose. If it fails, the error monitoring system
        # will log it and I'll learn how to harden it for the conductor env.
        customer = stripe.Customer.create(email=user.email, source=stripe_token)
        stripe.Subscription.create(
            customer=customer.id,
            items=[{"plan": settings.STRIPE_PLAN}],
            trial_from_plan=True,
        )
        return customer.id


stripe_gateway = StripeGateway()
