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
