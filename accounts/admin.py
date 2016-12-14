from django.contrib import admin

from accounts.models import InviteEmail, User


@admin.register(InviteEmail)
class InviteEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')
    search_fields = ['email']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
