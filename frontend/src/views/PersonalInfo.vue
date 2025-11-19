<script setup>
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
console.log(userStore)
const API_BASE = import.meta.env.VITE_API_BASE_URL

function goChangePassword() {
  window.location.href = `${API_BASE}/accounts/password/change/`
}

function goChangeEmail() {
  window.location.href = `${API_BASE}/accounts/email/`
}

</script>

<template>
  <div>
    <h2>Personal Info</h2>
    <p><strong>Username:</strong> {{ userStore.user?.username }}</p>
    <p><strong>Email:</strong> {{ userStore.user?.email }}</p>
    <p><strong>Subscription:</strong> {{ userStore.user?.subscription_info ? userStore.user.subscription_info.name : 'Not Subscribed' }}</p>
    <div v-if="!userStore.user?.is_social_login">
      <button class="account-button" :disabled="true" @click="goChangePassword">更改密碼</button>
      <button class="account-button" :disabled="true" @click="goChangeEmail">更改 Email</button>
    </div>
  </div>
</template>

<style scoped>
p {
  margin: 1rem 0;
  color: var(--color-text-3);
}

.account-button {
  color: #fff;
  padding: 0.5rem 1rem;
  margin: 0.5rem 1rem 0 0;
  background: var(--color-background-highlight-1);
  border-radius: 8px;
  border: 1px solid var(--color-background-highlight-2);
  cursor: pointer;
  font-weight: 600;
}

.account-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
