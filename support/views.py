from rest_framework import mixins, permissions, viewsets

from support.models import SupportTicket
from support.serializers import SupportTicketSerializer


class SupportTicketViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = (permissions.AllowAny,)
