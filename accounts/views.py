from rest_framework import mixins, permissions, viewsets

from accounts.models import InviteEmail
from accounts.serializers import InviteEmailSerializer


class InviteEmailViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = InviteEmail.objects.all()
    serializer_class = InviteEmailSerializer
    permission_classes = (permissions.AllowAny,)
