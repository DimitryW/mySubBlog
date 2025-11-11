# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from django_paddle_billing.models import Subscription
from allauth.socialaccount.models import SocialAccount


class UserSerializer(serializers.ModelSerializer):
    paddle_customer_id = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    subscription_info = serializers.SerializerMethodField()
    is_social_login = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "paddle_customer_id",
            "is_subscribed",
            "subscription_info",
            "is_social_login",
            "avatar",
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

    def get_is_social_login(self, obj):
        return SocialAccount.objects.filter(user=obj).exists()

    def get_avatar(self, obj):
        request = self.context.get("request")
        if hasattr(obj, "profile") and obj.profile.avatar:
            return request.build_absolute_uri(obj.profile.avatar.url)
        return (
            "https://storage.googleapis.com/dima-test1/static/images/default_avatar.png"
        )
