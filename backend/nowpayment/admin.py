from django.contrib import admin
from .models import NowPaymentSubscription


# Register your models here.
@admin.register(NowPaymentSubscription)
class NowPaymentSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "subscription_plan_id",
        "is_active",
        "status",
        "expire_date",
        "created_at",
        "updated_at",
    )
    search_fields = ("id", "user__username", "subscription_plan_id", "email")
    list_filter = ("is_active", "status", "created_at", "updated_at")
