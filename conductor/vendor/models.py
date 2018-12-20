from django.db import models


class PromptSchool(models.Model):
    """This model tracks the integration with Prompt's essay listing page."""

    name = models.TextField()
    slug = models.SlugField(max_length=512, unique=True)
    school = models.OneToOneField(
        "planner.School",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="prompt_school",
    )
