from rest_framework import serializers

from accounts.models import InviteEmail


class InviteEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteEmail
        fields = ('email',)
