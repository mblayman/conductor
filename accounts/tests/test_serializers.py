from unittest import mock

from django.contrib.auth import authenticate

from conductor.tests import TestCase
from accounts import serializers


class TestUserSerializer(TestCase):

    def test_serializes_id(self):
        user = self.UserFactory.create()
        serializer = serializers.UserSerializer(user)
        self.assertEqual(user.id, serializer.data['id'])

    def test_serializes_username(self):
        user = self.UserFactory.create()
        serializer = serializers.UserSerializer(user)
        self.assertEqual(user.username, serializer.data['username'])

    def test_serializes_email(self):
        user = self.UserFactory.create()
        serializer = serializers.UserSerializer(user)
        self.assertEqual(user.email, serializer.data['email'])

    def test_no_serialize_password(self):
        user = self.UserFactory.create()
        serializer = serializers.UserSerializer(user)
        self.assertNotIn('password', serializer.data.keys())

    @mock.patch('accounts.serializers.stripe_gateway')
    def test_creates_user(self, stripe_gateway):
        stripe_gateway.create_customer.return_value = 'cus_1234'
        validated_data = {
            'username': 'matt',
            'email': 'matt@test.com',
            'password': 'asecrettoeverybody',
            'stripe_token': 'tok_1234',
            'postal_code': '21702',
        }
        serializer = serializers.UserSerializer()

        user = serializer.create(validated_data)

        self.assertEqual(user.username, 'matt')
        self.assertEqual(user.email, 'matt@test.com')
        self.assertEqual(user.profile.postal_code, '21702')
        self.assertEqual(user.profile.stripe_customer_id, 'cus_1234')
        authenticated_user = authenticate(
            username='matt', password='asecrettoeverybody')
        self.assertEqual(user, authenticated_user)

    @mock.patch('accounts.serializers.stripe_gateway')
    def test_missing_postal_code(self, stripe_gateway):
        stripe_gateway.create_customer.return_value = 'cus_1234'
        validated_data = {
            'username': 'matt',
            'email': 'matt@test.com',
            'password': 'asecrettoeverybody',
            'stripe_token': 'tok_1234',
            'postal_code': None,
        }
        serializer = serializers.UserSerializer()

        user = serializer.create(validated_data)

        self.assertEqual(user.profile.postal_code, '')


class TestUserEmailSerializer(TestCase):

    def test_serializes_email(self):
        user = self.UserFactory.create()
        serializer = serializers.UserEmailSerializer(user)
        self.assertEqual(user.email, serializer.data['email'])


class TestUserUsernameSerializer(TestCase):

    def test_serializes_username(self):
        user = self.UserFactory.create()
        serializer = serializers.UserUsernameSerializer(user)
        self.assertEqual(user.username, serializer.data['username'])


class TestGoogleDriveAuthSerializer(TestCase):

    def test_serializes_id(self):
        auth = self.GoogleDriveAuthFactory.create()
        serializer = serializers.GoogleDriveAuthSerializer(auth)
        self.assertEqual(auth.id, serializer.data['id'])

    def test_no_serialize_code(self):
        auth = self.GoogleDriveAuthFactory.create()
        serializer = serializers.GoogleDriveAuthSerializer(auth)
        self.assertNotIn('code', serializer.data.keys())
