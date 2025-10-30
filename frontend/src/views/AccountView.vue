<script setup>
import { ref } from 'vue'
import PersonalInfo from './PersonalInfo.vue'
import PaymentHistory from './PaymentHistory.vue'

const activeTab = ref('info') // info 或 payments
</script>

<template>
  <div class="account-wrapper">
    <h1>Account</h1>
    <div class="account-content">
      <div class="tabs">
        <button :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">
          Personal Info
        </button>
        <button :class="{ active: activeTab === 'payments' }" @click="activeTab = 'payments'">
          Payment History
        </button>
      </div>

      <div class="tab-content">
        <PersonalInfo v-if="activeTab === 'info'" />
        <PaymentHistory v-if="activeTab === 'payments'" />
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  color: var(--color-text-2);
  height: 100px;
  width: 80%;
  font-weight: 600;
  margin: 0 auto;
  line-height: 100px;
}
.account-content {
  width: 80%;
  min-height: 800px;
  margin: 0 auto;
  color: var(--color-text-1);
  box-shadow: 0 10px 10px 5px rgba(0, 0, 0, 0.1);
  padding: 3rem 3rem 5rem;
  border-radius: 8px;
  background: var(--color-background-strong);
}
.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.tabs button {
  padding: 0.5rem 1rem;
  border: none;
  background: var(--color-background-soft);
  cursor: pointer;
  border-radius: 8px;
  color: var(--color-text-3);
}
.tabs button.active {
  background: var(--color-background-highlight-1);
  color: #fff;
  font-weight: 600;
}
.tab-content {
  padding: 1rem;
  background: var(--color-background-soft);
  border-radius: 8px;
}
</style>
