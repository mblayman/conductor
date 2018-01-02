from unittest import mock

from rest_framework.test import force_authenticate

from accounts import serializers, views
from conductor.tests import TestCase


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

    def test_unfiltered_list_empty(self):
        self.UserFactory.create()
        viewset = views.UserViewSet()
        viewset.action = 'list'
        viewset.request = self.request_factory.get()
        self.assertEqual(0, len(list(viewset.get_queryset())))

    def test_filters_username(self):
        self.UserFactory.create(username='burt')
        user = self.UserFactory.create(username='ernie')
        viewset = views.UserViewSet()
        viewset.action = 'list'
        viewset.request = self.request_factory.get(
            '/users?filter[username]=ernie')
        self.assertEqual([user], list(viewset.get_queryset()))

    def test_filters_email(self):
        self.UserFactory.create(email='burt@sesamestreet.com')
        user = self.UserFactory.create(email='ernie@sesamestreet.com')
        viewset = views.UserViewSet()
        viewset.action = 'list'
        viewset.request = self.request_factory.get(
            '/users?filter[email]=ernie@sesamestreet.com')
        self.assertEqual([user], list(viewset.get_queryset()))

    def test_email_filter_email_serializer(self):
        viewset = views.UserViewSet()
        viewset.request = self.request_factory.get(
            '/users?filter[email]=ernie@sesamestreet.com')
        self.assertEqual(
            serializers.UserEmailSerializer, viewset.get_serializer_class())

    def test_username_filter_username_serializer(self):
        viewset = views.UserViewSet()
        viewset.request = self.request_factory.get(
            '/users?filter[username]=ernie')
        self.assertEqual(
            serializers.UserUsernameSerializer, viewset.get_serializer_class())

    def test_serializer_gets_extra_data(self):
        serializer = mock.Mock()
        viewset = views.UserViewSet()
        viewset.request = self.request_factory.post()
        viewset.request.POST = {
            'postal_code': '21702',
            'stripe_token': 'tok_1234',
        }

        viewset.perform_create(serializer)

        serializer.save.assert_called_once_with(
            postal_code='21702', stripe_token='tok_1234')


class TestGoogleDriveAuthViewSet(TestCase):

    def _make_view(self):
        return views.GoogleDriveAuthViewSet.as_view(
            actions={'get': 'list', 'post': 'create'})

    def test_create(self):
        user = self.UserFactory.create()
        view = self._make_view()
        data = {'code': 'fake_auth_code'}
        request = self.request_factory.post(data=data)
        force_authenticate(request, user)

        response = view(request)

        self.assertEqual(201, response.status_code)

    def test_gets_user_auths(self):
        """For access control, a user can only get their auths."""
        user = self.UserFactory.create()
        auth = self.GoogleDriveAuthFactory.create(user=user)
        self.GoogleDriveAuthFactory.create()
        request = self.request_factory.authenticated_get(user)
        viewset = views.GoogleDriveAuthViewSet()
        viewset.request = request
        self.assertEqual([auth], list(viewset.queryset))
