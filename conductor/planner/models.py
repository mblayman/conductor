import os
import uuid

from django.conf import settings
from django.db import models
from localflavor.us.models import USStateField

from conductor.planner.managers import SchoolManager


class ApplicationSchedule(models.Model):
    """An application schedule represents the artifact that is exported.

    This could be done to Google Sheets.
    """

    created_date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        "Student", related_name="schedules", on_delete=models.CASCADE
    )


class Audit(models.Model):
    """An audit is used to keep a school's milestones up-to-date."""

    PENDING = "pending"
    COMPLETE = "complete"
    STATUS_CHOICES = ((PENDING, "Pending"), (COMPLETE, "Complete"))

    created_date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey("School", on_delete=models.CASCADE)
    semester = models.ForeignKey("Semester", on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=8)


class Milestone(models.Model):
    EARLY_DECISION = "ED"
    EARLY_DECISION_2 = "ED II"
    EARLY_ACTION = "EA"
    RESTRICTED_EARLY_ACTION = "REA"
    REGULAR_DECISION = "RD"
    CATEGORY_CHOICES = (
        (EARLY_DECISION, "Early Decision"),
        (EARLY_DECISION_2, "Early Decision II"),
        (EARLY_ACTION, "Early Action"),
        (RESTRICTED_EARLY_ACTION, "Restricted Early Action"),
        (REGULAR_DECISION, "Regular Decision"),
    )

    active = models.BooleanField(default=True)
    date = models.DateField()
    school = models.ForeignKey(
        "School", related_name="milestones", on_delete=models.CASCADE
    )
    category = models.CharField(
        choices=CATEGORY_CHOICES, default=REGULAR_DECISION, max_length=8
    )
    semester = models.ForeignKey(
        "Semester", related_name="milestones", on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return "{:%-m/%-d/%y}".format(self.date)


def school_image_path(instance: "School", filename: str) -> str:
    """Give each school a namespace and version.

    The goal is to make the images have long expiration headers.
    """
    name, ext = os.path.splitext(filename)
    return "schools/{}/{}{}".format(instance.slug, str(uuid.uuid4()), ext)


class School(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=256, unique=True)
    url = models.URLField(unique=True)
    milestones_url = models.URLField()
    rolling = models.BooleanField(default=False)
    city = models.CharField(max_length=128, null=True)
    state = USStateField(null=True)
    audit_notes = models.TextField(
        help_text="Notes to make performing audits easier", null=True, blank=True
    )
    # Using a regular FileField instead of ImageField to avoid bringing in Pillow.
    image = models.FileField(
        help_text="The school logo or seal at 400x400",
        upload_to=school_image_path,
        null=True,
        blank=True,
    )

    objects = SchoolManager()

    def __str__(self) -> str:
        return self.name


class Semester(models.Model):
    active = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self) -> str:
        season = "Fall"
        if self.date.month < 6:
            season = "Spring"
        elif self.date.month < 9:
            season = "Summer"
        return "{} {}".format(season, self.date.year)


class Student(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="students", on_delete=models.CASCADE
    )
    first_name = models.TextField()
    last_name = models.TextField()
    matriculation_semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    schools = models.ManyToManyField(School, through="TargetSchool")

    class Meta:
        ordering = ("id",)

    def __str__(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)


class TargetSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    milestones = models.ManyToManyField(Milestone)

    class Meta:
        ordering = ("id",)
        unique_together = ("school", "student")
