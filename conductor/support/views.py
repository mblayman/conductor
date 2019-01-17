from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from conductor.core.decorators import staff_required
from conductor.support.forms import SupportTicketForm
from conductor.trackers.models import CommonAppTracker


def contact(request: HttpRequest) -> HttpResponse:
    """Show a contact form."""
    if request.method == "POST":
        form = SupportTicketForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Thanks! We’ll get back to you soon."
            )
            return HttpResponseRedirect(reverse("contact"))
    else:
        form = SupportTicketForm()
    context = {"form": form}
    return render(request, "support/contact.html", context)


@staff_required
def tools_dashboard(request: HttpRequest) -> HttpResponse:
    """The entry point for all staff tools."""
    common_app_count = CommonAppTracker.objects.filter(
        status=CommonAppTracker.PENDING
    ).count()
    context: dict = {"common_app_count": common_app_count}
    return render(request, "support/tools_dashboard.html", context)
