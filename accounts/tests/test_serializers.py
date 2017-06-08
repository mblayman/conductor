from django.contrib.auth import authenticate

from conductor.tests import TestCase
from accounts import serializers


class TestInviteEmailSerializer(TestCase):

    def test_serializes_email(self):
        invite_email = self.InviteEmailFactory.create()
        serializer = serializers.InviteEmailSerializer(invite_email)
        self.assertEqual(invite_email.email, serializer.data['email'])


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

    def test_creates_user(self):
        validated_data = {
            'username': 'matt',
            'email': 'matt@test.com',
            'password': 'asecrettoeverybody',
        }
        serializer = serializers.UserSerializer()
        user = serializer.create(validated_data)
        self.assertEqual(user.username, 'matt')
        self.assertEqual(user.email, 'matt@test.com')
        authenticated_user = authenticate(
            username='matt', password='asecrettoeverybody')
        self.assertEqual(user, authenticated_user)


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
