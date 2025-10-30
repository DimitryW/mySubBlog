# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from django_paddle_billing.models import Subscription


class UserSerializer(serializers.ModelSerializer):
    paddle_customer_id = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    subscription_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "paddle_customer_id",
            "is_subscribed",
            "subscription_info",
        )

    def get_paddle_customer_id(self, obj):
        if hasattr(obj, "paddle_user"):
            return obj.paddle_user.paddle_customer_id
        return None

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(account=obj, status="active").exists()

    def get_subscription_info(self, obj):
        try:
            subscription = Subscription.objects.get(account=obj, status="active")
            return {
                "name": ", ".join(
                    [item["price"]["name"] for item in subscription.data["items"]]
                ),
                "status": subscription.status,
            }
        except Subscription.DoesNotExist:
            return None
