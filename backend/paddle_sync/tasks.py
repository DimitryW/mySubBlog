import re
import requests
from django.conf import settings
from celery import shared_task
from .models import PaddleUser
from django.contrib.auth.models import User
from .services import sync_products
from logging import getLogger

logger = getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def sync_products_task(self):
    """背景任務：同步 Paddle 產品資料"""
    try:
        sync_products()
        logger.info("[Paddle Sync] Products synced successfully.")
    except Exception as e:
        logger.error(f"[Paddle Sync] Error syncing products: {e}")
        # 延遲 60 秒後重試，最多重試 3 次
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def create_paddle_customer_task(self, user_id):
    """背景任務：建立 Paddle Customer 並同步到資料庫"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning(f"[Paddle Sync] User {user_id} not found.")
        return

    if PaddleUser.objects.filter(user=user).exists():
        logger.info(f"[Paddle Sync] PaddleUser already exists for {user.username}")
        return

    api_url = f"{settings.PADDLE_BILLING['PADDLE_API_URL']}/customers"
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_BILLING['PADDLE_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": user.email,
        "name": user.get_full_name() or user.username,
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        data = response.json().get("data", {})
        logger.debug(
            f"[Paddle Sync] Paddle customer response: {response.status_code}, {response.json()}"
        )

        if response.status_code in [200, 201]:
            paddle_id = data["id"]

        elif (
            response.status_code == 409
            and response.json().get("error", {}).get("code")
            == "customer_already_exists"
        ):
            match = re.search(r"customer of id (\w+)", response.text)
            paddle_id = match.group(1) if match else None

        elif response.status_code == 429:
            # Paddle Rate limit 限流，延後重試
            raise self.retry(exc=Exception("Rate limited"), countdown=60)

        else:
            logger.error(f"[Paddle Sync] Failed: {response.text}")
            raise self.retry(exc=Exception(response.text), countdown=10)

        if paddle_id:
            PaddleUser.objects.create(user=user, paddle_customer_id=paddle_id)
            logger.info(
                f"[Paddle Sync] Synced Paddle customer for {user.username}: {paddle_id}"
            )

    except requests.RequestException as e:
        logger.error(f"[Paddle Sync] Network error: {e}")
        raise self.retry(exc=e, countdown=15)
    except Exception as e:
        logger.exception(f"[Paddle Sync] Unexpected error: {e}")
        raise self.retry(exc=e, countdown=30)
