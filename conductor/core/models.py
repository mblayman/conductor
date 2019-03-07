from django.db import models
from django.utils import timezone
from waffle.models import AbstractUserFlag

from conductor.core.managers import SoftDeleteManager


class Flag(AbstractUserFlag):
    """Customizable version of Waffle's Flag model."""


class SoftDeleteModel(models.Model):
    """An abstract model to make a model soft deleteable."""

    deleted_date = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self) -> None:
        """Override delete and save the time when a model instance is deleted."""
        self.deleted_date = timezone.now()
        self.save()
