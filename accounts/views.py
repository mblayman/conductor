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


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsUser)
