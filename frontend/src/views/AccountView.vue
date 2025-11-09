<script setup>
import { ref } from 'vue'
import PersonalInfo from './PersonalInfo.vue'
import PaymentHistory from './PaymentHistory.vue'
import { uploadAvatar, avatarUrl } from '@/api/accountUsers.js'

const activeTab = ref('info') // info 或 payments
</script>

<template>
  <div class="account-wrapper">
    <h1>Account</h1>
    <div class="account-content">
      <div class="avatar-wrapper">
          <img
            v-if="avatarUrl"
            :src="avatarUrl"
            alt="大頭貼"
            class="avatar_img"
            @click="$refs.fileInput.click()"
          />
          <input type="file" @change="uploadAvatar" class="avatar_input" ref="fileInput"/>
      </div>
      <hr />

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

.avatar-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.avatar_img {
  border-radius: 50%;
  border: 2px solid var(--color-background-highlight-3);
  width: 5rem;
  height: 5rem;
  object-fit: cover;
  object-position: center;
}

.avatar_input {
  display: none;
}

hr {
  border: 0; 
  border-top: 1px solid var(--color-background-highlight-3); 
  margin: 1rem 0 2rem;
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
