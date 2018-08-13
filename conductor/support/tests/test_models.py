from conductor.tests import TestCase


class TestSupportTicket(TestCase):
    def test_factory(self) -> None:
        ticket = self.SupportTicketFactory.build()
        self.assertGreater(len(ticket.email), 0)
        self.assertGreater(len(ticket.subject), 0)
        self.assertGreater(len(ticket.message), 0)

    def test_str(self) -> None:
        ticket = self.SupportTicketFactory.build(subject="Halp!")
        self.assertEqual("Halp!", str(ticket))

    def test_has_email(self) -> None:
        ticket = self.SupportTicketFactory.build(email="matt@testing.com")
        self.assertEqual("matt@testing.com", ticket.email)

    def test_has_subject(self) -> None:
        ticket = self.SupportTicketFactory.build(subject="Halp!")
        self.assertEqual("Halp!", ticket.subject)

    def test_has_message(self) -> None:
        ticket = self.SupportTicketFactory.build(message="How do you do?")
        self.assertEqual("How do you do?", ticket.message)
