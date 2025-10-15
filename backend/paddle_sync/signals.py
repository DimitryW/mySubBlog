import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PaddleUser


@receiver(post_save, sender=User)
def create_paddle_customer(sender, instance, created, **kwargs):
    """在用戶註冊後，自動同步到 Paddle 建立 Customer"""
    if not created:
        return

    # 如果已經有 PaddleUser，跳過
    if PaddleUser.objects.filter(user=instance).exists():
        return

    api_url = f"{settings.PADDLE_BILLING['PADDLE_API_URL']}/customers"
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_BILLING['PADDLE_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": instance.email,
        "name": instance.get_full_name() or instance.username,
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        data = response.json().get("data", {})
        print(response.status_code, response.json())
        if response.status_code in [200, 201]:
            paddle_id = data["id"]
        elif (
            response.status_code == 409
            and response.json().get("error").get("code") == "customer_already_exists"
        ):
            # 已存在，從錯誤訊息中抓 id
            import re

            match = re.search(r"customer of id (\w+)", response.text)
            paddle_id = match.group(1) if match else None
        else:
            print(f"[Paddle Sync] Failed to create Paddle customer: {response.text}")
            return

        if paddle_id:
            PaddleUser.objects.create(user=instance, paddle_customer_id=paddle_id)
            print(
                f"[Paddle Sync] Synced Paddle customer for {instance.username}: {paddle_id}"
            )

    except Exception as e:
        print(f"[Paddle Sync] Exception when creating Paddle customer: {e}")
