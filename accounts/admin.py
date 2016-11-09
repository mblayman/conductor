from django.contrib import admin

from accounts.models import InviteEmail


@admin.register(InviteEmail)
class InviteEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')
    search_fields = ['email']
