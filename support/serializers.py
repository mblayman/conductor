from rest_framework_json_api import serializers

from support.models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ('email', 'subject', 'message')
