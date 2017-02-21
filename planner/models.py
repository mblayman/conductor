import datetime

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from localflavor.us.models import USStateField


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
    date = models.DateTimeField()
    school = models.ForeignKey(
        'School', related_name='milestones', on_delete=models.CASCADE)
    category = models.CharField(
        choices=CATEGORY_CHOICES, default=REGULAR_DECISION, max_length=8)


@python_2_unicode_compatible
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

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Semester(models.Model):
    active = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return str(self.date)


# XXX: This is locked in for the default value of the initial migration.
# I'm not sure what needs to be done to let me safely delete this and
# have migrations continue to work.
def current_year():
    today = datetime.date.today()
    return today.year


@python_2_unicode_compatible
class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='students')
    first_name = models.TextField()
    last_name = models.TextField()
    matriculation_semester = models.ForeignKey(
        Semester, on_delete=models.PROTECT)
    schools = models.ManyToManyField(School, through='TargetSchool')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class TargetSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('school', 'student')
