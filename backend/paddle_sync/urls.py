# accounts/urls.py
from django.urls import path
from django_paddle_billing.views import paddle_webhook_view


urlpatterns = [
    path("webhook/", paddle_webhook_view, name="paddle-webhook"),
]
