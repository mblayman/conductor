from django.conf import settings
from django.contrib.auth.decorators import user_passes_test


def check_if_staff(user: settings.AUTH_USER_MODEL) -> bool:
    """Check if the user has staff permissions."""
    return user.is_staff


staff_required = user_passes_test(check_if_staff)
