from django.db import models


class Milestone(models.Model):
    date = models.DateTimeField()


class School(models.Model):
    name = models.TextField()
    url = models.URLField()
