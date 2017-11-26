from django.contrib import admin

from accounts.models import Profile, User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
