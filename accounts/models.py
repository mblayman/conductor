from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """The central user model.

    This is a user defined model rather than the default Django User
    to permit easy extension while avoiding joins on other tables.
    """
