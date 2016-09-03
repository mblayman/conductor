from rest_framework import permissions

from accounts import views
from conductor.tests import TestCase


class TestInviteEmailViewSet(TestCase):

    def test_no_retrieve(self):
        """Sanity check that no retrieve method is available."""
        viewset = views.InviteEmailViewSet()
        self.assertRaises(AttributeError, lambda: viewset.retrieve)

    def test_allow_any(self):
        viewset = views.InviteEmailViewSet()
        self.assertIn(permissions.AllowAny, viewset.permission_classes)
