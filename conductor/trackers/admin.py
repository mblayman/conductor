from django.contrib import admin

from conductor.trackers.models import CommonAppTracker


@admin.register(CommonAppTracker)
class CommonAppTrackerAdmin(admin.ModelAdmin):
    list_display = ("name",)
