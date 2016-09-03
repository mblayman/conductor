from conductor.tests import TestCase
from accounts import serializers


class TestInviteEmailSerializer(TestCase):

    def test_serializes_email(self):
        invite_email = self.InviteEmailFactory.create()
        serializer = serializers.InviteEmailSerializer(invite_email)
        self.assertEqual(invite_email.email, serializer.data['email'])
