from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """The central user model.

    This is a user defined model rather than the default Django User
    to permit easy extension while avoiding joins on other tables.
    """
    # Override the default definition to make the email required and unique.
    email = models.EmailField(_('email address'), blank=False, unique=True)


class Profile(models.Model):
    """Additional data about a user.

    This data is information about a user that is needed infrequently.
    The intent is to pull this on rare occasions like looking up Stripe info.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    postal_code = models.CharField(
        max_length=32,
        blank=True,
    )
    stripe_customer_id = models.CharField(
        max_length=32,
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """Create a profile for a new user."""
    if created:
        Profile.objects.create(user=instance)
