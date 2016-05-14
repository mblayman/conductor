from rest_framework import mixins, viewsets

from support.models import SupportTicket
from support.serializers import SupportTicketSerializer


class SupportTicketViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
