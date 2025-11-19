from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NowPaymentSubscription(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True
    )  # NowPayments 的 subscription id

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="nowpayment_subscriptions"
    )

    subscription_plan_id = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ("WAITING_PAY", "Waiting Pay"),
        ("PAID", "Paid"),
        ("PARTIALLY_PAID", "Partially Paid"),
        ("EXPIRED", "Expired"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    expire_date = models.DateTimeField(null=True, blank=True)

    # subscriber.email
    email = models.EmailField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    raw = models.JSONField(default=dict)

    def __str__(self):
        return f"NP-{self.id} ({self.status})"
