from rest_framework import permissions

from conductor.tests import TestCase
from support import views


class TestSupportTicketViewSet(TestCase):

    def test_no_retrieve(self):
        """Sanity check that no retrieve method is available."""
        viewset = views.SupportTicketViewSet()
        self.assertRaises(AttributeError, lambda: viewset.retrieve)

    def test_allow_any(self):
        viewset = views.SupportTicketViewSet()
        self.assertIn(permissions.AllowAny, viewset.permission_classes)
