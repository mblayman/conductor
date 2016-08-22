from rest_framework import viewsets

from planner.models import School
from planner.serializers import SchoolSerializer, StudentSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return self.request.user.students.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
