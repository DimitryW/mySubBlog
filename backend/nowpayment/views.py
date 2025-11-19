# nowpayment/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
from django.conf import settings
from decouple import config
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
import json
from django.utils import timezone
import json, hmac, hashlib
from decouple import config
from .models import NowPaymentSubscription
from django.utils.dateparse import parse_datetime

logger = logging.getLogger(__name__)


def serialize_nowpayment_subscription(sub: NowPaymentSubscription):
    return {
        "id": sub.id,
        "customer_email": sub.email,
        "name": f"{sub.subscription_plan_id}",
        "price": "",
        "price_id": sub.subscription_plan_id,
        "next_payment": (
            sub.expire_date.strftime("%Y-%m-%d") if sub.expire_date else None
        ),
        "status": sub.status,
        "desc": "",
        "is_active": sub.is_active,
        "created_at": sub.created_at,
        "updated_at": sub.updated_at,
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_subscription(request):
    user = request.user
    subscriptions = NowPaymentSubscription.objects.filter(user=user)
    if subscriptions.exists():
        data = serialize_nowpayment_subscription(subscriptions.first())
    else:
        data = {}
    return Response(data)


def verify_nowpayments_signature(request, secret):
    np_sig = request.headers.get("x-nowpayments-sig")
    body = json.loads(request.body)
    sorted_body = json.dumps(body, separators=(",", ":"), sort_keys=True)
    signature = hmac.new(
        secret.encode(), sorted_body.encode(), hashlib.sha512
    ).hexdigest()
    return hmac.compare_digest(signature, np_sig)


def get_nowpayments_token():
    url = "https://api.nowpayments.io/v1/auth"
    payload = {
        "email": config("NOWPAYMENT_EMAIL"),
        "password": config("NOWPAYMENT_PASSWORD"),
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json().get("token")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    """
    前端傳: { plan_id }
    """
    plan_id = request.data.get("plan_id")
    if not plan_id:
        return Response({"error": "plan_id required"}, status=400)

    token = get_nowpayments_token()
    url = "https://api.nowpayments.io/v1/subscriptions"
    payload = {"subscription_plan_id": plan_id, "email": request.user.email}
    headers = {
        "Authorization": f"Bearer {token}",
        "x-api-key": config("NOWPAYMENT_API_KEY"),
        "Content-Type": "application/json",
    }

    resp = requests.post(url, json=payload, headers=headers)
    data = resp.json()

    # 建立 Model
    sub = NowPaymentSubscription.objects.create(
        id=data["result"][0]["id"],
        user=request.user,
        subscription_plan_id=data["result"][0]["subscription_plan_id"],
        is_active=data["result"][0]["is_active"],
        status=data["result"][0]["status"],
        expire_date=parse_datetime(data["result"][0]["expire_date"]),
        email=data["result"][0]["subscriber"]["email"],
        created_at=parse_datetime(data["result"][0]["created_at"]),
        updated_at=parse_datetime(data["result"][0]["updated_at"]),
    )
    return Response(resp.json())


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def nowpayment_webhook(request):
    """接收 NOWPayments 的 webhook 通知，驗證簽章後更新狀態"""
    try:
        data = json.loads(request.body)
        logger.info(f"[NOWPayments webhook] Valid webhook: {data}")

        # Step 1: 驗證簽章
        secret = config("NOWPAYMENT_IPN_SECRET")
        if not verify_nowpayments_signature(request, secret):
            logger.warning("[NOWPayments webhook] Invalid signature")
            return Response({"error": "Invalid signature"}, status=403)

        # Step 2: 解析資料

        # payment_status = data.get("payment_status")
        # order_id = data.get("order_id")
        # pay_amount = data.get("pay_amount")
        # pay_currency = data.get("pay_currency")
        # payment_id = data.get("payment_id")

        # # Step 3: 根據業務邏輯更新訂閱狀態
        # from subscriptions.models import Subscription  # 假設你有 Subscription model

        # sub = Subscription.objects.filter(order_id=order_id).first()
        # if not sub:
        #     logger.warning(f"Subscription not found for order_id={order_id}")
        #     return Response({"error": "Subscription not found"}, status=404)

        # status_map = {
        #     "waiting": "pending",
        #     "confirming": "pending",
        #     "confirmed": "active",
        #     "finished": "active",
        #     "failed": "failed",
        #     "expired": "canceled",
        # }

        # new_status = status_map.get(payment_status, "unknown")
        # sub.status = new_status
        # sub.payment_id = payment_id
        # sub.pay_amount = pay_amount
        # sub.pay_currency = pay_currency
        # sub.updated_at = timezone.now()
        # sub.save()

        # logger.info(f"Subscription {sub.id} updated to {new_status}")

        return Response({"result": "ok"}, status=200)

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        return Response({"error": str(e)}, status=500)
