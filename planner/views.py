from rest_framework import viewsets
from rest_framework_json_api.pagination import PageNumberPagination
from rest_framework_json_api.views import ModelViewSet

from planner.models import School, Semester
from planner.serializers import (
    SchoolSerializer, SemesterSerializer, StudentSerializer)


class SchoolPagination(PageNumberPagination):
    page_size = 12


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    pagination_class = SchoolPagination


class SemesterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Semester.objects.all().filter(active=True)
    serializer_class = SemesterSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer

    @property
    def queryset(self):
        return self.request.user.students.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
