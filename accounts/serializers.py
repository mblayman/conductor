from rest_framework_json_api import serializers

from accounts.models import InviteEmail, User


class InviteEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteEmail
        fields = ('email',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )
