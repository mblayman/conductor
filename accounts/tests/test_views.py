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


class TestUserViewSet(TestCase):

    def _make_view(self):
        return views.UserViewSet.as_view(actions={'get': 'retrieve'})

    def test_retrieve(self):
        user = self.UserFactory.create()
        request = self.request_factory.authenticated_get(user)
        view = self._make_view()
        response = view(request, pk=user.id)
        self.assertEqual(200, response.status_code)

    def test_other_user_retrieve(self):
        user = self.UserFactory.create()
        other_user = self.UserFactory.create()
        request = self.request_factory.authenticated_get(other_user)
        view = self._make_view()
        response = view(request, pk=user.id)
        self.assertEqual(403, response.status_code)
