import os

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from accounts.views import dashboard, signup, user_settings
from planner.views import add_school, add_student, student_profile
from support.views import contact


urlpatterns = [
    # Marketing/non-authenticated views
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('signup/', signup, name='signup'),
    path('contact/', contact, name='contact'),
    path('terms/',
         TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('privacy/',
         TemplateView.as_view(template_name='privacy.html'), name='privacy'),

    path('app/', dashboard, name='dashboard'),
    path('settings/', user_settings, name='settings'),

    # Students
    path('students/add/', add_student, name='add-student'),
    path('students/<int:student_id>/',
         student_profile, name='student-profile'),
    path('students/<int:student_id>/add-school/',
         add_school, name='add-school'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if os.environ['DJANGO_SETTINGS_MODULE'] == 'conductor.settings.development':
    import debug_toolbar
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += staticfiles_urlpatterns()
