from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class SupportTicket(models.Model):
    subject = models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.subject
