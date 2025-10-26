# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from django_paddle_billing.models import Subscription


class UserSerializer(serializers.ModelSerializer):
    paddle_customer_id = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "paddle_customer_id", "is_subscribed")

    def get_paddle_customer_id(self, obj):
        if hasattr(obj, "paddle_user"):
            return obj.paddle_user.paddle_customer_id
        return None

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(account=obj, status="active").exists()
