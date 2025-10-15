// src/api/accountUsers.js
import { ref } from 'vue'
const API_BASE = import.meta.env.VITE_API_BASE_URL

export const isLoggedIn = ref(false)
export const username = ref('')

// 取得登入狀態
export async function fetchUser() {
  try {
    const res = await fetch(`${API_BASE}/api/user/info`, { credentials: 'include' })
    const data = await res.json()
    isLoggedIn.value = !!data.username
    username.value = data.username || ''
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
