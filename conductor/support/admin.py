from django.contrib import admin

from conductor.support.models import SupportTicket


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('email', 'subject')
    search_fields = ['email']
