from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from conductor.planner.models import (
    ApplicationSchedule,
    Audit,
    Milestone,
    School,
    SchoolApplication,
    Semester,
    Student,
    TargetSchool,
)


@admin.register(ApplicationSchedule)
class ApplicationScheduleAdmin(admin.ModelAdmin):
    list_display = ("created_date",)


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ("school", "created_date", "status")
    list_filter = ("status",)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("school", "date", "category")


class AuditInline(admin.StackedInline):
    model = Audit
    extra = 0


class MilestoneInline(admin.StackedInline):
    model = Milestone


class SchoolApplicationInline(admin.StackedInline):
    model = SchoolApplication


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    def clickable_url(obj: School) -> str:
        return format_html('<a href="{0}" target="_blank">{1}</a>', obj.url, obj.url)

    clickable_url.short_description = "url"  # type: ignore  # noqa mypy/708

    list_display = ("name", clickable_url, "milestones_url")
    list_per_page = 10
    ordering = ["id"]
    search_fields = ["name"]

    inlines = [AuditInline, MilestoneInline, SchoolApplicationInline]


@admin.register(SchoolApplication)
class SchoolApplicationAdmin(admin.ModelAdmin):
    list_display = ("school", "application_type")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("date", "active")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "matriculation_semester")


@admin.register(TargetSchool)
class TargetSchoolAdmin(admin.ModelAdmin):
    list_display = ("student", "school", "deleted_date")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return self.model.all_objects.all()
