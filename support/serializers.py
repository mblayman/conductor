from rest_framework import serializers

from support.models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ('subject', 'message')
