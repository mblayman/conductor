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
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
        )


class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )
