from rest_framework import viewsets

from planner.models import School
from planner.serializers import SchoolSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
