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

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from accounts.views import GoogleDriveAuthViewSet, UserViewSet
from planner.views import (
    ApplicationStatusViewSet, MilestoneViewSet, SchoolViewSet, SemesterViewSet,
    StudentViewSet, TargetSchoolViewSet)
from support.views import SupportTicketViewSet
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
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', ObtainJSONWebToken.as_view()),
    url(r'^api-token-refresh/', RefreshJSONWebToken.as_view()),
]

if os.environ['DJANGO_SETTINGS_MODULE'] == 'conductor.settings.development':
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
