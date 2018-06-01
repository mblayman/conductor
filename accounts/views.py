from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets

from accounts.forms import SignupForm
from accounts.models import GoogleDriveAuth, User
from accounts.serializers import (
    GoogleDriveAuthSerializer, UserSerializer, UserEmailSerializer,
    UserUsernameSerializer)


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
    return render(request, 'accounts/dashboard.html', {})


class IsUser(permissions.BasePermission):
    """Only the user can access their own information."""

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)

    @property
    def queryset(self):
        # Retrieve looks at all users, but the identity permissions protect
        # from getting any other user's data.
        if self.action == 'retrieve':
            return User.objects.all()
        # Only list users when filtering on username or email.
        # This is made safe by having custom serializers when filtering
        # on either of these fields that return very little information.
        if 'filter[username]' in self.request.query_params:
            return User.objects.filter(
                username=self.request.query_params['filter[username]'])
        if 'filter[email]' in self.request.query_params:
            return User.objects.filter(
                email=self.request.query_params['filter[email]'])
        return User.objects.none()

    def get_serializer_class(self):
        """Get the serializer class.

        The custom serializers for username and email are to ensure
        that extra user data does not leak out if someone is scanning for it.
        """
        if 'filter[username]' in self.request.query_params:
            return UserUsernameSerializer
        if 'filter[email]' in self.request.query_params:
            return UserEmailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = (permissions.IsAuthenticated, IsUser)
        return super(UserViewSet, self).get_permissions()

    def perform_create(self, serializer):
        """Give the serializer the Stripe token when creating."""
        stripe_token = self.request.POST.get('stripe_token')
        postal_code = self.request.POST.get('postal_code')
        serializer.save(stripe_token=stripe_token, postal_code=postal_code)


class GoogleDriveAuthViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = GoogleDriveAuthSerializer

    @property
    def queryset(self):
        user = self.request.user
        return GoogleDriveAuth.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
