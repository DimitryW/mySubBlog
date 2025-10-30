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
