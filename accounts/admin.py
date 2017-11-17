from django.contrib import admin

from accounts.models import InviteEmail, Profile, User


@admin.register(InviteEmail)
class InviteEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')
    search_fields = ['email']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
