from django.db import models


class PromptSchool(models.Model):
    """The model tracks the integration with Prompts essay listing page."""

    name = models.TextField()
    slug = models.SlugField(max_length=512, unique=True)
    school = models.ForeignKey(
        "planner.School", null=True, blank=True, on_delete=models.SET_NULL
    )
