from rest_framework import mixins, permissions, viewsets

from accounts.models import InviteEmail, User
from accounts.serializers import InviteEmailSerializer, UserSerializer


class InviteEmailViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = InviteEmail.objects.all()
    serializer_class = InviteEmailSerializer
    permission_classes = (permissions.AllowAny,)


class IsUser(permissions.BasePermission):
    """Only the user can access their own information."""

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
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
        # TODO: Make this comment statement true.
        if 'filter[username]' in self.request.query_params:
            return User.objects.filter(
                username=self.request.query_params['filter[username]'])
        if 'filter[email]' in self.request.query_params:
            return User.objects.filter(
                email=self.request.query_params['filter[email]'])
        return User.objects.none()

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = (permissions.IsAuthenticated, IsUser)
        return super(UserViewSet, self).get_permissions()
