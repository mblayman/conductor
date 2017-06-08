from rest_framework import mixins, permissions, viewsets

from accounts.models import InviteEmail, User
from accounts.serializers import (
    InviteEmailSerializer, UserSerializer, UserEmailSerializer,
    UserUsernameSerializer)


class InviteEmailViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = InviteEmail.objects.all()
    serializer_class = InviteEmailSerializer
    permission_classes = (permissions.AllowAny,)


class IsUser(permissions.BasePermission):
    """Only the user can access their own information."""

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)

    @property
    def queryset(self):
        # Retrieve looks at all users, but the identity permissions protect
        # from getting any other user's data.
        if self.action == 'retrieve':
            return User.objects.all()
        # Only list users when filtering on username or email.
        # This is made safe by having custom serializers when filtering
        # on either of these fields that return very little information.
        if 'filter[username]' in self.request.query_params:
            return User.objects.filter(
                username=self.request.query_params['filter[username]'])
        if 'filter[email]' in self.request.query_params:
            return User.objects.filter(
                email=self.request.query_params['filter[email]'])
        return User.objects.none()

    def get_serializer_class(self):
        """Get the serializer class.

        The custom serializers for username and email are to ensure
        that extra user data does not leak out if someone is scanning for it.
        """
        if 'filter[username]' in self.request.query_params:
            return UserUsernameSerializer
        if 'filter[email]' in self.request.query_params:
            return UserEmailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = (permissions.IsAuthenticated, IsUser)
        return super(UserViewSet, self).get_permissions()
