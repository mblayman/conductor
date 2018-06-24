import os

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from accounts.views import dashboard, signup
from planner.views import add_school, add_student, student_profile
from support.views import contact
from vendor.views import ObtainJSONWebToken, RefreshJSONWebToken


urlpatterns = [
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
    url(r'^api-token-auth/', ObtainJSONWebToken.as_view()),
    url(r'^api-token-refresh/', RefreshJSONWebToken.as_view()),
]

if os.environ['DJANGO_SETTINGS_MODULE'] == 'conductor.settings.development':
    import debug_toolbar
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += staticfiles_urlpatterns()
