from conductor.tests import TestCase
from support import serializers


class TestSupportTicketSerializer(TestCase):

    def test_serializes_email(self):
        ticket = self.SupportTicketFactory.create()
        serializer = serializers.SupportTicketSerializer(ticket)
        self.assertEqual(ticket.email, serializer.data['email'])

    def test_serializes_subject(self):
        ticket = self.SupportTicketFactory.create()
        serializer = serializers.SupportTicketSerializer(ticket)
        self.assertEqual(ticket.subject, serializer.data['subject'])

    def test_serializes_message(self):
        ticket = self.SupportTicketFactory.create()
        serializer = serializers.SupportTicketSerializer(ticket)
        self.assertEqual(ticket.message, serializer.data['message'])
