# paddle_sync/models.py
from django.db import models
from django.contrib.auth.models import User


class PaddleUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="paddle_user"
    )
    paddle_customer_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.paddle_customer_id})"
