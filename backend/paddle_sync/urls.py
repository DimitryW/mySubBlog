# accounts/urls.py
from django.urls import path
from django_paddle_billing.views import paddle_webhook_view
from .views import my_subscription, change_subscription


urlpatterns = [
    path("webhook/", paddle_webhook_view, name="paddle-webhook"),
    path("my-subscription/", my_subscription, name="my-subscription"),
    path("change-subscription/", change_subscription, name="change-subscription"),
]
