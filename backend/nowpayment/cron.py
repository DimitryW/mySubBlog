import requests
from decouple import config
from .models import NowPaymentSubscription
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def sync_nowpayment_subscriptions(last_days=30):
    url = "https://api.nowpayments.io/v1/subscriptions"
    headers = {"x-api-key": config("NOWPAYMENT_API_KEY")}

    all_plans = NowPaymentSubscription.objects.values_list(
        "subscription_plan_id", flat=True
    ).distinct()

    cutoff_date = timezone.now() - timedelta(days=last_days)
    logger.info(f"Start syncing NOWPayments subscriptions. Cutoff date: {cutoff_date}")

    for plan_id in all_plans:
        limit = 100
        offset = 0

        while True:
            params = {
                "subscription_plan_id": plan_id,
                "status": "PAID",
                "limit": limit,
                "offset": offset,
            }

            resp = requests.get(url, headers=headers, params=params)
            data = resp.json()

            if "result" not in data or not data["result"]:
                break

            recent_items = [
                item
                for item in data["result"]
                if parse_datetime(item["updated_at"]) >= cutoff_date
            ]

            if not recent_items:
                break

            for item in recent_items:
                sub_id = item["id"]

                try:
                    sub = NowPaymentSubscription.objects.get(id=sub_id)
                except NowPaymentSubscription.DoesNotExist:
                    continue

                # 更新狀態
                sub.status = item["status"]
                sub.is_active = item["is_active"]
                sub.expire_date = parse_datetime(item.get("expire_date"))
                sub.updated_at = parse_datetime(item.get("updated_at"))
                sub.raw = item

                sub.save()
                logger.info(
                    f"Updated subscription: {sub_id}: "
                    f"status: {sub.status}, "
                    f"is_active: {sub.is_active}, "
                    f"expire_date: {sub.expire_date}"
                )

            offset += limit
    logger.info("NOWPayments subscription sync completed.")
