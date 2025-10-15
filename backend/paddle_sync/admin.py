from django.contrib import admin
from .models import PaddleUser


@admin.register(PaddleUser)
class PaddleUserAdmin(admin.ModelAdmin):
    list_display = ("user", "paddle_customer_id", "created_at")
    search_fields = ("user__username", "paddle_customer_id")
