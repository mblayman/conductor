from django.contrib import admin

from conductor.vendor.models import PromptSchool


@admin.register(PromptSchool)
class PromptSchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "school")
    raw_id_fields = ("school",)
