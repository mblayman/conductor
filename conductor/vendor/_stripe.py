from django.conf import settings
import stripe

from conductor.accounts.models import ProductPlan
from conductor.core.exceptions import ConductorError

stripe.api_key = settings.STRIPE_API_KEY


class StripeGateway:
    """A gateway to Stripe

    This insulates the rest of the system from Stripe errors
    and configures the Stripe module with the API key.
    """

    def create_customer(
        self,
        user: settings.AUTH_USER_MODEL,
        stripe_token: str,
        product_plan: ProductPlan,
    ) -> str:
        """Add a user to Stripe and join them to the plan."""
        # Let this fail on purpose. If it fails, the error monitoring system
        # will log it and I'll learn how to harden it for the conductor env.
        customer = stripe.Customer.create(email=user.email, source=stripe_token)
        stripe.Subscription.create(
            customer=customer.id,
            items=[{"plan": product_plan.stripe_plan_id}],
            trial_from_plan=True,
        )
        return customer.id

    def cancel_subscription(self, user: settings.AUTH_USER_MODEL) -> None:
        """Cancel the user's Stripe subscription."""
        try:
            customer = stripe.Customer.retrieve(user.profile.stripe_customer_id)
            subscription_id = customer.subscriptions.data[0].id
            subscription = stripe.Subscription.retrieve(subscription_id)
            subscription.delete()
        except stripe.error.StripeError as ex:
            raise ConductorError() from ex


stripe_gateway = StripeGateway()
