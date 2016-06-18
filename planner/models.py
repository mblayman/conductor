import datetime

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class Milestone(models.Model):
    date = models.DateTimeField()


@python_2_unicode_compatible
class School(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=256, unique=True)
    url = models.URLField(unique=True)
    milestones_url = models.URLField()

    def __str__(self):
        return self.name


def current_year():
    today = datetime.date.today()
    return today.year


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_name = models.TextField()
    last_name = models.TextField()
    class_year = models.IntegerField(default=current_year)
