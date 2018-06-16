"""conductor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

from accounts.views import (
    GoogleDriveAuthViewSet, UserViewSet, dashboard, signup)
from planner.views import (
    ApplicationStatusViewSet, MilestoneViewSet, SchoolViewSet, SemesterViewSet,
    StudentViewSet, TargetSchoolViewSet,
    add_school, add_student, student_profile)
from support.views import SupportTicketViewSet, contact
from vendor.views import ObtainJSONWebToken, RefreshJSONWebToken

router = routers.DefaultRouter(trailing_slash=False)
router.register(
    'application-statuses', ApplicationStatusViewSet,
    base_name='applicationstatus')
router.register(
    'google-drive-auths',
    GoogleDriveAuthViewSet,
    base_name='googledriveauth')
router.register('milestones', MilestoneViewSet)
router.register('schools', SchoolViewSet, base_name='school')
router.register('semesters', SemesterViewSet)
router.register('support-tickets', SupportTicketViewSet)
router.register('students', StudentViewSet, base_name='student')
router.register(
    'target-schools', TargetSchoolViewSet, base_name='targetschool')
router.register('users', UserViewSet, base_name='user')

urlpatterns = [
    # TODO: Remove this when the API is removed.
    # url(r'^', include(router.urls)),
    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='index'),
    url(r'^signup/$',
        signup,
        name='signup'),
    url(r'^app/$',
        dashboard,
        name='dashboard'),
    url(r'^contact/$',
        contact,
        name='contact'),
    url(r'^terms/$',
        TemplateView.as_view(template_name='terms.html'),
        name='terms'),
    url(r'^privacy/$',
        TemplateView.as_view(template_name='privacy.html'),
        name='privacy'),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^students/add/',
        add_student,
        name='add-student'),
    url(r'^students/(?P<student_id>\d+)/$',
        student_profile,
        name='student-profile'),
    url(r'^students/(?P<student_id>\d+)/add-school/',
        add_school,
        name='add-school'),

    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', ObtainJSONWebToken.as_view()),
    url(r'^api-token-refresh/', RefreshJSONWebToken.as_view()),
]

if os.environ['DJANGO_SETTINGS_MODULE'] == 'conductor.settings.development':
    import debug_toolbar
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += staticfiles_urlpatterns()
