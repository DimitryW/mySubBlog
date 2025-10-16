# accounts/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("info/", views.user_info, name="api_user_info"),
    path("logout/", views.logout_view, name="api_logout"),
]
