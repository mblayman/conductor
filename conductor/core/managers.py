from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """Override delete to perform a soft delete."""

    def delete(self) -> int:
        """Override delete with update to permit bulk deletes."""
        return super().update(deleted_date=timezone.now())


class SoftDeleteManager(models.Manager):
    """A manager to handle soft deletion."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model).filter(deleted_date=None)
