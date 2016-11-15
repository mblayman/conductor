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
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from accounts.views import InviteEmailViewSet
from planner.views import SchoolViewSet, SemesterViewSet, StudentViewSet
from support.views import SupportTicketViewSet
from vendor.views import ObtainJSONWebToken, RefreshJSONWebToken

router = routers.DefaultRouter(trailing_slash=False)
router.register('invite-emails', InviteEmailViewSet)
router.register('schools', SchoolViewSet)
router.register('semesters', SemesterViewSet)
router.register('support-tickets', SupportTicketViewSet)
router.register('students', StudentViewSet, base_name='student')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', ObtainJSONWebToken.as_view()),
    url(r'^api-token-refresh/', RefreshJSONWebToken.as_view()),
]
