// src/api/accountUsers.js
import axios from "axios";
import { ref } from 'vue'
import { getCookie } from './utils';
const API_BASE = import.meta.env.VITE_API_BASE_URL

export const isLoggedIn = ref(false)
export const username = ref('')
export const is_subscribed = ref(false)
export const avatarUrl = ref(null)

// 取得登入狀態
export async function fetchUser() {
  try {
    const res = await fetch(`${API_BASE}/api/user/info`, { credentials: 'include' })
    const data = await res.json()
    isLoggedIn.value = !!data.username
    username.value = data.username || ''
    is_subscribed.value = data.is_subscribed || false
    avatarUrl.value = data.avatar || null
    console.log('User fetched:', data)
    return data
  } catch (err) {
    console.error('Fetch user failed', err)
    return null
  }
}

// 登入（導向 Django allauth login 頁面）
export function login() {
  window.location.href = `${API_BASE}/accounts/login/`  // 或加上 next/?redirect=
}

// 登出
export function logout() {
  window.location.href = `${API_BASE}/accounts/logout/`
}

export const uploadAvatar = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append("avatar", file)

  const res = await axios.post(`${API_BASE}/api/user/upload-avatar/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
    withCredentials: true,
    headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  })
  window.location.reload()
}