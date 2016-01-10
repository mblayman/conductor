from django.db import models


class Milestone(models.Model):
    date = models.DateTimeField()


class School(models.Model):
    name = models.TextField()
    slug = models.SlugField(max_length=256, unique=True)
    url = models.URLField()
    milestones_url = models.URLField()
