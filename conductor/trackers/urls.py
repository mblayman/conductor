from django.urls import path

from conductor.trackers import views

app_name = "trackers"
urlpatterns = [
    path("connect-common-apps/", views.connect_common_apps, name="connect-common-apps")
]
