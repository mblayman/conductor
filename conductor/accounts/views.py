from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from google_auth_oauthlib.flow import Flow

from conductor.accounts.forms import SignupForm
from conductor.accounts.models import GoogleDriveAuth, ProductPlan


def index(request: HttpRequest) -> HttpResponse:
    """The landing page."""
    product_plan = ProductPlan.objects.filter(active=True).last()
    context = {"product_plan": product_plan}
    return render(request, "index.html", context)


def signup(request: HttpRequest) -> HttpResponse:
    """Sign up a new user."""
    product_plan = ProductPlan.objects.filter(active=True).last()

    if request.method == "POST":
        form = SignupForm(product_plan, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "errors": dict(form.errors.items())})

    context = {
        "product_plan": product_plan,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, "accounts/signup.html", context)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Show the main view for an authenticated user."""
    students = (
        request.user.students.all()
        .select_related("matriculation_semester")
        .order_by("last_name")
    )
    context = {"app_nav": "dashboard", "students": students}
    return render(request, "accounts/dashboard.html", context)


@login_required
def user_settings(request: HttpRequest) -> HttpResponse:
    """Show the user's settings options."""
    context = {"app_nav": "settings"}
    return render(request, "accounts/settings.html", context)


@login_required
def authorize_google(request: HttpRequest) -> HttpResponseRedirect:
    """Build and present an auth URL to get permission to use Google Drive."""
    flow = Flow.from_client_config(
        settings.GOOGLE_CLIENT_CONFIG,
        scopes=GoogleDriveAuth.SCOPES,
        redirect_uri=settings.GOOGLE_CLIENT_CONFIG["web"]["redirect_uris"][0],
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", prompt="consent"
    )
    request.session["state"] = state
    return HttpResponseRedirect(authorization_url)


@login_required
def oauth2_callback(request: HttpRequest) -> HttpResponseRedirect:
    """Handle the callback from Google to create an authorization."""
    if request.GET.get("error"):
        messages.add_message(
            request,
            messages.ERROR,
            "We weren’t able to complete authorization with Google.",
        )
        return HttpResponseRedirect(reverse("settings"))

    state = request.session.pop("state", "")
    flow = Flow.from_client_config(
        settings.GOOGLE_CLIENT_CONFIG,
        scopes=GoogleDriveAuth.SCOPES,
        redirect_uri=settings.GOOGLE_CLIENT_CONFIG["web"]["redirect_uris"][0],
        state=state,
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    GoogleDriveAuth.objects.create(
        user=request.user, refresh_token=credentials.refresh_token
    )

    return HttpResponseRedirect(reverse("settings"))
