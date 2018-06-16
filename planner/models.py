import datetime

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from localflavor.us.models import USStateField

from planner.managers import SchoolManager


class ApplicationStatus(models.Model):
    """An application status represents the artifact that is exported.

    This could be done to Google Sheets.
    """
    created_date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        'Student',
        related_name='schedules',
        on_delete=models.CASCADE
    )


class Audit(models.Model):
    """An audit is used to keep a school's milestones up-to-date."""
    PENDING = 'pending'
    COMPLETE = 'complete'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
    )

    created_date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    status = models.CharField(
        choices=STATUS_CHOICES, default=PENDING, max_length=8)


class Milestone(models.Model):
    EARLY_DECISION = 'ED'
    EARLY_DECISION_1 = 'ED1'
    EARLY_DECISION_2 = 'ED2'
    EARLY_ACTION = 'EA'
    REGULAR_DECISION = 'RD'
    CATEGORY_CHOICES = (
        (EARLY_DECISION, 'Early Decision'),
        (EARLY_DECISION_1, 'Early Decision 1'),
        (EARLY_DECISION_2, 'Early Decision 2'),
        (EARLY_ACTION, 'Early Action'),
        (REGULAR_DECISION, 'Regular Decision'),
    )

    active = models.BooleanField(default=True)
    date = models.DateField()
    school = models.ForeignKey(
        'School', related_name='milestones', on_delete=models.CASCADE)
    category = models.CharField(
        choices=CATEGORY_CHOICES, default=REGULAR_DECISION, max_length=8)

    def __str__(self):
        return '{:%-m/%-d/%y}'.format(self.date)


class School(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=256, unique=True)
    url = models.URLField(unique=True)
    milestones_url = models.URLField()
    rolling = models.BooleanField(default=False)
    city = models.CharField(max_length=128, null=True)
    state = USStateField(null=True)
    audit_notes = models.TextField(
        help_text='Notes to make performing audits easier',
        null=True, blank=True)

    objects = SchoolManager()

    def __str__(self):
        return self.name

    @cached_property
    def milestones_dict(self):
        """Get the active milestones keyed by category."""
        milestones = self.milestones.filter(active=True).all()
        return {milestone.category: milestone for milestone in milestones}

    @property
    def early_decision(self):
        return self.milestones_dict.get(Milestone.EARLY_DECISION)

    @property
    def early_decision_1(self):
        return self.milestones_dict.get(Milestone.EARLY_DECISION_1)

    @property
    def early_decision_2(self):
        return self.milestones_dict.get(Milestone.EARLY_DECISION_2)

    @property
    def early_action(self):
        return self.milestones_dict.get(Milestone.EARLY_ACTION)

    @property
    def regular_decision(self):
        return self.milestones_dict.get(Milestone.REGULAR_DECISION)


class Semester(models.Model):
    active = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        season = 'Fall'
        if self.date.month < 6:
            season = 'Spring'
        elif self.date.month < 9:
            season = 'Summer'
        return '{} {}'.format(season, self.date.year)


# XXX: This is locked in for the default value of the initial migration.
# I'm not sure what needs to be done to let me safely delete this and
# have migrations continue to work.
def current_year():
    today = datetime.date.today()
    return today.year


class Student(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='students',
        on_delete=models.CASCADE
    )
    first_name = models.TextField()
    last_name = models.TextField()
    matriculation_semester = models.ForeignKey(
        Semester, on_delete=models.PROTECT)
    schools = models.ManyToManyField(School, through='TargetSchool')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class TargetSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('school', 'student')
