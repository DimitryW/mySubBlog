# accounts/urls.py
from django.urls import path
from . import views
from django_paddle_billing.views import paddle_webhook_view


urlpatterns = [
    path("info/", views.user_info, name="api_user_info"),
    path("logout/", views.logout_view, name="api_logout"),
    path("webhook/", paddle_webhook_view, name="paddle-webhook"),
]
