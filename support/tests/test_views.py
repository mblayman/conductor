from conductor.tests import TestCase
from support import views


class TestSupportTicketViewSet(TestCase):

    def test_no_retrieve(self):
        """Sanity check that no retrieve method is available."""
        viewset = views.SupportTicketViewSet()
        self.assertRaises(AttributeError, lambda: viewset.retrieve)
