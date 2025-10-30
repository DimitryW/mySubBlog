# paddle_sync/views.py
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_paddle_billing.models import Subscription, Transaction, Customer
import requests
from django.conf import settings


def serialize_subscription(sub):
    try:
        item = sub.data.get("items", [])[0] if sub.data else []
        name = item["price"]["name"]
        unit_prices = int(item["price"]["unit_price"]["amount"]) / 100
        frequencies = f"{item['price']['billing_cycle']['interval']}"
        price = f"{unit_prices}/{frequencies}"
        price_id = item["price"]["id"]
        next_payment = sub.data.get("next_billed_at")[:10] if sub.data else None
        desc = item["price"]["description"]
    except Exception:
        name, price, next_payment, desc = "", "", None, ""

    return {
        "id": sub.id,
        "customer_email": sub.customer.email if sub.customer else None,
        "name": name,
        "price": price,
        "price_id": price_id,
        "next_payment": next_payment,
        "status": sub.status,
        "desc": desc,
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_subscription(request):
    user = request.user
    subscriptions = Subscription.objects.filter(account=user).exclude(status="canceled")
    if subscriptions.exists():
        data = serialize_subscription(subscriptions.first())
    else:
        data = {}
    return Response(data)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_subscription(request):
    """
    body: { subscription_id, new_price_id, proration_billing_mode }
    """
    subscription_id = request.data.get("subscription_id")
    new_price_id = request.data.get("new_price_id")
    proration_billing_mode = request.data.get(
        "proration_billing_mode", "prorated_immediately"
    )

    if not subscription_id or not new_price_id:
        return Response(
            {"error": "subscription_id and new_price_id required"}, status=400
        )

    api_url = (
        f"{settings.PADDLE_BILLING['PADDLE_API_URL']}/subscriptions/{subscription_id}"
    )
    headers = {
        "Authorization": f"Bearer {settings.PADDLE_BILLING['PADDLE_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "proration_billing_mode": proration_billing_mode,
        "items": [{"price_id": new_price_id, "quantity": 1}],
    }
    resp = requests.patch(api_url, json=payload, headers=headers)
    return Response(resp.json())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_transactions(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    if not customer:
        return Response([])

    transactions = customer.transactions.all().order_by("-created_at")

    data = []
    for tx in transactions:
        # 付款金額
        amount = 0
        if tx.data:
            try:
                amount = int(tx.data["details"]["totals"]["total"]) / 100
            except Exception:
                pass
        tx_type = "payment" if amount >= 0 else "refund/adjustment"

        # 付款日期
        date = ""
        if tx.data:
            try:
                date = tx.data["payments"][0]["captured_at"]
            except Exception:
                pass

        # 狀態
        status = ""
        if tx.data:
            status = tx.data.get("status", "")

        # 付款方式
        method = ""
        if tx.data.get("payments"):
            method = f'{tx.data["payments"][0]["method_details"]["card"]["type"]} {tx.data["payments"][0]["method_details"]["card"]["last4"]}'

        data.append(
            {
                "id": tx.id,
                "date_paid": date,
                "payment_amount": amount,
                "status": status,
                "type": tx_type,
                "method": method,
            }
        )

    return Response(data)
