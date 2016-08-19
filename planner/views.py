from rest_framework import viewsets

from planner.models import School, Student
from planner.serializers import SchoolSerializer, StudentSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
