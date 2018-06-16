import functools
import operator

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_json_api.pagination import PageNumberPagination
from rest_framework_json_api.views import ModelViewSet

from planner import tasks
from planner.forms import AddSchoolForm, AddStudentForm
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


@login_required
def add_student(request):
    """Add a student to the user's set."""
    if request.method == 'POST':
        form = AddStudentForm(data=request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = AddStudentForm()
    context = {
        'app_nav': 'add-student',
        'form': form,
    }
    return render(request, 'planner/add_student.html', context)


@login_required
def student_profile(request, student_id):
    """Show a student's information."""
    student = get_object_or_404(
        request.user.students.select_related('matriculation_semester'),
        id=student_id)
    schools = student.schools.all().order_by('name')
    context = {
        'student': student,
        'schools': schools,
    }
    return render(request, 'planner/student_profile.html', context)


@login_required
def add_school(request, student_id):
    """Add a school to a student's list."""
    student = get_object_or_404(request.user.students, id=student_id)
    query = request.GET.get('q')

    if request.method == 'POST':
        form = AddSchoolForm(student, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('student-profile', args=[student.id]))
    else:
        form = AddSchoolForm(student)

    schools = []
    if query:
        schools = School.objects.search(query)

    context = {
        'q': query,
        'form': form,
        'schools': schools,
        'student': student,
    }
    return render(request, 'planner/add_school.html', context)
