from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """The central user model.

    This is a user defined model rather than the default Django User
    to permit easy extension while avoiding joins on other tables.
    """


class InviteEmail(models.Model):
    """Record emails for interested people."""
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)
