from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from accounts.forms import SignupForm


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
