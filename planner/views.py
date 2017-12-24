import functools
import operator

from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_json_api.pagination import PageNumberPagination
from rest_framework_json_api.views import ModelViewSet

from planner import tasks
from planner.models import (
    ApplicationStatus, Milestone, School, Semester, TargetSchool)
from planner.serializers import (
    ApplicationStatusSerializer, MilestoneSerializer, SchoolSerializer,
    SemesterSerializer, StudentSerializer, TargetSchoolSerializer)


class ApplicationStatusViewSet(ModelViewSet):
    serializer_class = ApplicationStatusSerializer

    @property
    def queryset(self):
        user = self.request.user
        return ApplicationStatus.objects.filter(student__user=user)


class MilestoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Milestone.objects.all().filter(active=True)
    serializer_class = MilestoneSerializer


class SchoolPagination(PageNumberPagination):
    page_size = 12


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SchoolSerializer
    pagination_class = SchoolPagination

    @property
    def queryset(self):
        queryset = School.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            terms = [SearchQuery(term) for term in search.split()]
            vector = SearchVector('name')
            query = functools.reduce(operator.or_, terms)
            queryset = queryset.annotate(
                rank=SearchRank(vector, query)).order_by('-rank')
            # This is a magic value. By inspecting rank,
            # it appeared that anything below 0.04 was junk.
            queryset = queryset.filter(rank__gte=0.04)
        return queryset


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


class TargetSchoolViewSet(ModelViewSet):
    serializer_class = TargetSchoolSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('school', 'student')

    @property
    def queryset(self):
        return TargetSchool.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        tasks.audit_school.delay(instance.school_id)
