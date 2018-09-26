from collections import OrderedDict
import json
from typing import List, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from conductor.planner.forms import AddSchoolForm, AddStudentForm
from conductor.planner.models import Milestone, School, SchoolApplication
from conductor.planner.tasks import build_schedule


def school_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Show details about a school."""
    school = get_object_or_404(School, slug=slug)
    if request.user.is_authenticated:
        template = "planner/school.html"
    else:
        template = "planner/school_unauthenticated.html"
    context = {"school": school}
    return render(request, template, context)


@login_required
def add_student(request: HttpRequest) -> HttpResponse:
    """Add a student to the user's set."""
    if request.method == "POST":
        form = AddStudentForm(data=request.POST)
        if form.is_valid():
            student = form.save(request.user)
            redirect_url = reverse("student-profile", args=[student.id])
            return HttpResponseRedirect(redirect_url)
    else:
        form = AddStudentForm()
    context = {"app_nav": "add-student", "form": form}
    return render(request, "planner/add_student.html", context)


@login_required
def student_profile(request: HttpRequest, student_id: int) -> HttpResponse:
    """Show a student's information."""
    student = get_object_or_404(
        request.user.students.select_related("matriculation_semester"), id=student_id
    )

    schools = student.schools.all()
    prefetch = Prefetch(
        "milestones",
        queryset=Milestone.objects.filter(semester=student.matriculation_semester),
    )
    schools = schools.prefetch_related(prefetch, "applications").order_by("name")

    target_milestone_ids = student.schools.through.objects.filter(
        student=student
    ).values_list("milestones", flat=True)
    target_milestones = Milestone.objects.filter(id__in=target_milestone_ids)

    target_school_applications_ids = student.schools.through.objects.filter(
        student=student
    ).values_list("school_application", flat=True)
    target_school_applications = set(
        SchoolApplication.objects.filter(id__in=target_school_applications_ids)
    )

    # Group the schools by application type and order them
    # with the most prevalent first.
    schools_by_application_type = {
        application_type[1]: []
        for application_type in SchoolApplication.APPLICATION_TYPE_CHOICES
    }
    for school in schools:
        school_applications_set = set(school.applications.all())
        # Check if the student has a selected application type for the school.
        no_app_selected = target_school_applications.isdisjoint(school_applications_set)
        for school_application in school.applications.all():
            app_school = {
                "school": school,
                "no_app_selected": no_app_selected,
                "selected": school_application in target_school_applications,
            }
            schools_by_application_type[
                school_application.get_application_type_display()
            ].append(app_school)
    schools_by_application_type = OrderedDict(
        sorted(
            schools_by_application_type.items(), key=lambda x: len(x[1]), reverse=True
        )
    )

    context = {
        "Milestone": Milestone,
        "student": student,
        "schools": schools,
        "schools_by_application_type": schools_by_application_type,
        "target_milestones": target_milestones,
    }
    return render(request, "planner/student_profile.html", context)


@login_required
def add_school(request: HttpRequest, student_id: int) -> HttpResponse:
    """Add a school to a student's list."""
    student = get_object_or_404(request.user.students, id=student_id)
    query = request.GET.get("q")

    if request.method == "POST":
        form = AddSchoolForm(student, data=request.POST)
        if form.is_valid():
            form.save()
            redirect_url = reverse("student-profile", args=[student.id])
            return HttpResponseRedirect(redirect_url)
    else:
        form = AddSchoolForm(student)

    schools: Union[List[School], QuerySet] = []
    if query:
        schools = School.objects.search(query)

    context = {"q": query, "form": form, "schools": schools, "student": student}
    return render(request, "planner/add_school.html", context)


@login_required
def export_schedule(request: HttpRequest, student_id: int) -> HttpResponseRedirect:
    """Trigger a schedule export."""
    student = get_object_or_404(request.user.students, id=student_id)

    if not request.user.has_google_drive_auth:
        messages.add_message(
            request,
            messages.INFO,
            "We need your permission to access Google Drive before exporting.",
        )
        return HttpResponseRedirect(reverse("settings"))

    build_schedule.delay(student.id)

    messages.add_message(
        request,
        messages.SUCCESS,
        "We’re exporting the schedule to Google Drive. It will be ready in a moment.",
    )
    redirect_url = reverse("student-profile", args=[student.id])
    return HttpResponseRedirect(redirect_url)


@login_required
@require_POST
def set_student_milestone(request: HttpRequest, student_id: int) -> JsonResponse:
    """Set a milestone for a target school.

    Add or remove the milestone depending on whether or not it is set.
    """
    student = get_object_or_404(request.user.students, id=student_id)
    data = json.loads(request.body)
    milestone = get_object_or_404(
        Milestone.objects.all().select_related("school"), id=data["milestone"]
    )

    target_school = get_object_or_404(
        student.schools.through, student=student, school=milestone.school
    )
    action = ""
    if target_school.milestones.filter(id=milestone.id).exists():
        target_school.milestones.remove(milestone)
        action = "remove"
    else:
        target_school.milestones.add(milestone)
        action = "add"

    return JsonResponse({"status": "success", "action": action})
