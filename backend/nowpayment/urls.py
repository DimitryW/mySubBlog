# nowpayment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("create-subscription/", views.create_subscription),
    path("my-subscription/", views.my_subscription),
    path("webhook/", views.nowpayment_webhook, name="nowpayment_webhook"),
]
