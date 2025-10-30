<script setup>
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
console.log(userStore)
</script>

<template>
  <div>
    <h2>Personal Info</h2>
    <p><strong>Username:</strong> {{ userStore.user?.username }}</p>
    <p><strong>Email:</strong> {{ userStore.user?.email }}</p>
    <p><strong>Subscription:</strong> {{ userStore.user?.subscription_info ? userStore.user.subscription_info.name : '' }}</p>
  </div>
</template>

<style scoped>
p {
  margin: 1rem 0;
  color: var(--color-text-3);
}
</style>
