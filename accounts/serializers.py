from rest_framework_json_api import serializers

from accounts.models import InviteEmail


class InviteEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteEmail
        fields = ('email',)
