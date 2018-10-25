from collections import namedtuple

from django.db import models


RawCommonAppSchool = namedtuple("RawCommonAppSchool", ["name", "slug"])


class CommonAppTracker(models.Model):
    """Track Common Application schools.

    This data is for tracking of scans of the Common App website.
    """

    PENDING = 1
    TRACKED = 2
    INTERNATIONAL = 3
    UNTRACKED = 4
    REMOVED = 5
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (TRACKED, "Tracked"),
        (INTERNATIONAL, "International"),
        (UNTRACKED, "Untracked"),
        (REMOVED, "Removed"),
    )

    created_date = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    slug = models.SlugField(max_length=512, unique=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=PENDING)
    school = models.ForeignKey(
        "planner.School", null=True, blank=True, on_delete=models.SET_NULL
    )
