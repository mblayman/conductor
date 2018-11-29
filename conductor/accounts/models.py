from typing import Any, Dict

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from google.oauth2.credentials import Credentials


class User(AbstractUser):
    """The central user model.

    This is a user defined model rather than the default Django User
    to permit easy extension while avoiding joins on other tables.
    """

    # Override the default definition to make the email required and unique.
    email = models.EmailField(_("email address"), blank=False, unique=True)

    @property
    def has_google_drive_auth(self) -> bool:
        """Check if the user has authorized Google Drive."""
        return self.google_drive_authorizations.exists()


class Profile(models.Model):
    """Additional data about a user.

    This data is information about a user that is needed infrequently.
    The intent is to pull this on rare occasions like looking up Stripe info.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=32, blank=True)
    stripe_customer_id = models.CharField(max_length=32)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(
    sender: User, instance: Profile, created: bool, **kwargs: Any
) -> None:
    """Create a profile for a new user."""
    if created:
        Profile.objects.create(user=instance)


class GoogleDriveAuth(models.Model):
    """Store authorization information for Google Drive.

    This model stores the authorized tokens required to do exports
    to Google Sheets.
    """

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="google_drive_authorizations",
        on_delete=models.CASCADE,
    )
    refresh_token = models.TextField(help_text="For renewing the token validity")

    @property
    def credentials(self) -> Credentials:
        """Get Google credentials."""
        return Credentials.from_authorized_user_info(
            self.authorized_user_info, scopes=self.SCOPES
        )

    @property
    def authorized_user_info(self) -> Dict[str, str]:
        """Get the authorized data required to generate valid credentials."""
        return {
            "refresh_token": self.refresh_token,
            "client_id": settings.GOOGLE_CLIENT_CONFIG["web"]["client_id"],
            "client_secret": settings.GOOGLE_CLIENT_CONFIG["web"]["client_secret"],
        }


class ProductPlan(models.Model):
    """A container referencing Stripe product plans."""

    active = models.BooleanField(default=False)
    stripe_plan_id = models.CharField(max_length=32)
    trial_days = models.IntegerField(default=0)
    price = models.IntegerField(default=0, help_text="The price in cents")

    @property
    def display_price(self) -> str:
        """Get the price in a nicely formatted way."""
        dollars = self.price / 100
        return f"${dollars:.2f}"
