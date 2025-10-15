<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/user'
import { LogIn, LogOut, Home, Info, CreditCard, User } from 'lucide-vue-next'
import { isLoggedIn, username, login, logout, fetchUser } from '../src/api/accountUsers.js'

const userStore = useUserStore()
const API_BASE = import.meta.env.VITE_API_BASE_URL
const isDark = ref(false)

function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

async function loadUser() {
  const data = await fetchUser()
  userStore.setUser(data)
  console.log('user')
  console.log(data)
}

// 深色模式：讀取使用者偏好 or 系統預設
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  } else {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  document.documentElement.classList.toggle('dark', isDark.value)

  loadUser()
})
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
       <!-- 🌙 切換按鈕 -->
        <div class="theme-switch" @click="toggleTheme">
          <span class="switch-label">{{ isDark ? '🌙 Dark' : '☀️ Light' }}</span>
          <div class="switch-track">
            <div class="switch-thumb" :class="{ dark: isDark }"></div>
          </div>
        </div>

        <div class="login" v-if="isLoggedIn">
          <a @click="logout"><LogOut class="icon" />Logout</a>
        </div>
        <div class="logout" v-else>
          <a @click="login"><LogIn class="icon" />Login</a>
        </div>

        <RouterLink to="/">
          <Home class="icon" /> Home
        </RouterLink>
        <RouterLink v-if="isLoggedIn" to="/subscription">
          <CreditCard class="icon" /> My Subscription
        </RouterLink>
        <!--
        <RouterLink v-if="isLoggedIn" to="/account">
          <User class="icon" /> Account
        </RouterLink>
        -->
        <RouterLink to="/about">
          <Info class="icon" /> About
        </RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  background: var(--color-background-soft);
  padding: 10px 40px;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a  {
  width: 100%;
  margin: 0 auto;
}

/* active 狀態 */
nav a.router-link-exact-active {
  /* background: #424242ff; */   /* 淺灰底色 */
  background: var(--color-background-highlight-1);
  color: #fff;             /* 白字 */
  border-radius: 10px;      /* 圓角邊邊 */
  font-weight: 600;
}

nav a {
  color: var(--color-text-2);
  display: flex;
  align-items: center; 
  gap: 0.5rem; 
  padding: 1rem;
  margin: 1rem 0.5rem;
  height: 50px;
  font-size: 14px;
}

/* hover 效果 */
nav a:hover {
  background: var(--color-background-highlight-2);
  border-radius: 10px;      /* 圓角邊邊 */
}

/* 切換按鈕樣式 */
.theme-switch {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  user-select: none;
  margin: 16px 16px 32px 32px;
}

.switch-track {
  width: 50px;
  height: 24px;
  background: var(--color-background-highlight-1);
  border-radius: 999px;
  position: relative;
  transition: background 0.3s;
}

.switch-thumb {
  width: 20px;
  height: 20px;
  background: var(--color-background);
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: left 0.3s, background 0.3s;
}

.switch-thumb.dark {
  left: 28px; /* 移到右邊 */
  background: #FAA634; /* 右邊可換顏色，像黃色太陽 */
}

.switch-label {
  font-size: 14px;
  color: var(--color-text-1);
}


@media (min-width: 1024px) {
  header {
    display: block;
    padding-left: calc(var(--section-gap) / 8);
    border-right: 1px solid var(--color-background-highlight-2);
    padding-bottom: 2rem;
    max-width: 245px;
}

  nav a .icon {
  width: 18px;   /* 控制 icon 大小 */
  height: 18px;
}

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
