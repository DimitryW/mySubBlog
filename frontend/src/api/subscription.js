// api/subscription.js
import axios from "axios";
import { getCookie } from './utils';
const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function fetchMySubscription() {
  const res = await axios.get(`${API_BASE}/api/paddle/my-subscription/`, {
    withCredentials: true,
  });
  console.log("Response:", res);
  return res.data;
}

export async function changeSubscription(subscriptionId, newPriceId) {
  console.log("Changing subscription:", subscriptionId, newPriceId);

  const res = await axios.post(`${API_BASE}/api/paddle/change-subscription/`, {
    subscription_id: subscriptionId,
    new_price_id: newPriceId,
  }, {
    withCredentials: true,
    headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  });
  console.log("Response:", res);
  return res.data;
}

export async function fetchMyTransactions() {
  const res = await axios.get(`${API_BASE}/api/paddle/my-transactions/`, {
    withCredentials: true,
  });
  console.log("Response:", res);
  return res.data; 
}

export async function payWithCrypto(planId) {
  try {
    const res = await axios.post(`${API_BASE}/api/nowpayment/create-subscription/`, {
      plan_id: planId,
    }, {
      withCredentials: true,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const data = await res.data;
    console.log("NowPayments subscription response:", data);

    if (data.result && data.result.length > 0) {
      const sub = data.result[0];
      if (sub.status === "WAITING_PAY") {
        alert(
          `Subscription created! Please pay for your plan.\nSubscriber: ${sub.subscriber.email}`
        );
        // 如果你有回傳支付 URL，這裡可以直接跳轉
        // window.location.href = sub.payment_url;
      } else if (sub.is_active) {
        alert("Subscription is active!");
      }
    } else {
      alert("Failed to create subscription.");
    }
  } catch (err) {
    console.error("Failed to create subscription:", err);
    alert("Error creating subscription.");
  }
}

