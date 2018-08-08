from django.contrib import admin
from django.utils.html import format_html

from conductor.planner.models import (
    Audit, Milestone, School, Semester, Student, TargetSchool)


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('school', 'created_date', 'status')
    list_filter = ('status',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('school', 'date', 'category')


class MilestoneInline(admin.StackedInline):
    model = Milestone


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    def clickable_url(obj):
        return format_html(
            '<a href="{0}" target="_blank">{1}</a>', obj.url, obj.url)
    clickable_url.short_description = 'url'

    list_display = ('name', clickable_url, 'milestones_url')
    list_per_page = 10
    ordering = ['id']
    search_fields = ['name']

    inlines = [
        MilestoneInline,
    ]


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('date', 'active')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'matriculation_semester')


@admin.register(TargetSchool)
class TargetSchoolAdmin(admin.ModelAdmin):
    list_display = ('student', 'school')
