# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from paddle_sync.models import PaddleUser


class UserSerializer(serializers.ModelSerializer):
    paddle_customer_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "paddle_customer_id")

    def get_paddle_customer_id(self, obj):
        if hasattr(obj, "paddle_user"):
            return obj.paddle_user.paddle_customer_id
        return None
