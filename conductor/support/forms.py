from django import forms

from conductor.support.models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    """A form to let users contact the site to submit a ticket."""

    class Meta:
        model = SupportTicket
        fields = "__all__"
