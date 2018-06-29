from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from google_auth_oauthlib.flow import Flow

from accounts.forms import SignupForm
from accounts.models import GoogleDriveAuth


def signup(request):
    """Sign up a new user."""
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'success'})
        return JsonResponse({
            'status': 'error',
            'errors': dict(form.errors.items()),
        })

    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def dashboard(request):
    """Show the main view for an authenticated user."""
    students = request.user.students.all().select_related(
        'matriculation_semester').order_by('last_name')
    context = {
        'app_nav': 'dashboard',
        'students': students,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def user_settings(request):
    """Show the user's settings options."""
    context = {
        'app_nav': 'settings',
    }
    return render(request, 'accounts/settings.html', context)


@login_required
def authorize_google(request):
    """Build and present an auth URL to get permission to use Google Drive."""
    flow = Flow.from_client_config(
        settings.GOOGLE_CLIENT_CONFIG,
        scopes=['https://www.googleapis.com/auth/drive.file'])
    # TODO: Put the state in the session so that the callback can validate it.
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true', prompt='consent')
    return HttpResponseRedirect(authorization_url)


@login_required
def oauth2_callback(request):
    """Handle the callback from Google to create an authorization."""
    # TODO: Do what it promises.
    GoogleDriveAuth.objects.create(
        user=request.user, code=request.GET.get('code'))
    context = {
        'app_nav': 'settings',
    }
    return render(request, 'accounts/settings.html', context)
