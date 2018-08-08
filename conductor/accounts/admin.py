from django.contrib import admin

from conductor.accounts.models import GoogleDriveAuth, Profile, User


@admin.register(GoogleDriveAuth)
class GoogleDriveAuthAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
