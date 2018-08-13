from django.db import models


class SupportTicket(models.Model):
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()

    def __str__(self) -> str:
        return self.subject
