from django.contrib import admin

from planner.models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ['name']
