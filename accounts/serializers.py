from rest_framework_json_api import serializers

from accounts.models import User
from vendor.services import stripe_gateway


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
        """Create a new Stripe customer and conductor user."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])

        # Before persisting anything, make sure that the customer creation
        # happens with Stripe.
        stripe_customer_id = stripe_gateway.create_customer(
            user, validated_data['stripe_token'])

        user.save()

        user.profile.stripe_customer_id = stripe_customer_id
        if validated_data['postal_code']:
            user.profile.postal_code = validated_data['postal_code']
        user.profile.save()

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
