<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/user'
import { Sun, Moon, LogIn, LogOut, Home, Info, CreditCard, User, BookMarked, LayoutList, MessageCircle } from 'lucide-vue-next'
import { isLoggedIn, username, login, logout, fetchUser } from '@/api/accountUsers.js'

const userStore = useUserStore()
const API_BASE = import.meta.env.VITE_API_BASE_URL
const isDark = ref(false)
const isMenuOpen = ref(false)

function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

function toggleMenu() { // 漢堡選單切換
  isMenuOpen.value = !isMenuOpen.value
}

async function loadUser() {
  const data = await fetchUser()
  userStore.setUser(data)
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
    <div class="logo-wrapper">
      <RouterLink to="/">
        <img class="logo-img" src="/site_logo.jpg" alt="Dimitry's Digest Logo"/>
        <div class="title">Dimitry's Digest</div>
      </RouterLink>
    </div> 
    <hr>
    <div class="wrapper">
       <div class="nav-top-wrapper">
       <!-- 上方區塊：深色切換 + 登入按鈕 -->
        <div class="nav-top">
          <div class="theme-switch" @click="toggleTheme">
            <div class="switch-icon">
              <component :is="isDark ? Moon : Sun" class="icon" />
            </div>
            <div class="switch-track">
              <div class="switch-thumb" :class="{ dark: isDark }"></div>
            </div>
          </div>

          <div v-if="isLoggedIn" class="auth-btn">
            <a @click="logout"><LogOut class="icon" />Logout</a>
          </div>
          <div v-else class="auth-btn">
            <a @click="login"><LogIn class="icon" />Login</a>
          </div>
        </div>
        </div>

        <!-- 漢堡按鈕 -->
        <button class="hamburger" @click="toggleMenu">
          <span :class="{ open: isMenuOpen }"></span>
          <span :class="{ open: isMenuOpen }"></span>
          <span :class="{ open: isMenuOpen }"></span>
        </button>

      <nav :class="{ open: isMenuOpen }">
        <RouterLink to="/">
          <Home class="icon" /> Home
        </RouterLink>

        <RouterLink to="/categories">
          <LayoutList class="icon" /> Categories
        </RouterLink>

        <RouterLink v-if="isLoggedIn" to="/subscription">
          <CreditCard class="icon" /> Subscription
        </RouterLink>

        <RouterLink v-if="isLoggedIn" to="/account">
          <User class="icon" /> Account
        </RouterLink>

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
  border-right: 1px solid var(--color-background-highlight-2);
}

header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

.logo-wrapper {
  width: 100%;
  text-align: center;
}

.logo-img {
  border-radius: 50%;
  border: 2px solid var(--color-background-highlight-3);
  width: 5rem;
  height: 5rem;
  object-fit: cover;
  object-position: center;
}

.title {
  font-size: 1.3rem;
  color: var(--color-text-2);
  font-weight: 600;
}

hr {
  border: 0; 
  border-top: 1px solid var(--color-background-highlight-3); 
  margin: 0 0 2rem;
  }

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
}

.nav-top {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between; /* 左右排列 */
  margin: 0.5rem 0 1.5rem;
  font-weight: 600;
  font-size: 0.8rem;
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
  margin: 0.5rem 0;
  height: 50px;
  font-size: 14px;
}

/* hover 效果 */
nav a:hover {
  background: var(--color-background-highlight-2);
  border-radius: 10px;      /* 圓角邊邊 */
}

.auth-btn a {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-2);
  cursor: pointer;
}

.auth-btn a:hover {
  background: none !important;
  border-radius: none !important;
}

/* 切換按鈕樣式 */
.theme-switch {
  display: flex;
  align-items: center;
  gap: 0.6rem; /* 讓太陽/月亮與開關間有距離 */
  cursor: pointer;
  user-select: none;
}

.switch-icon .icon {
  width: 18px;
  height: 18px;
  color: var(--color-text-2);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.switch-track {
  width: 50px;
  height: 18px;
  background: var(--color-background-highlight-1);
  border-radius: 999px;
  position: relative;
  transition: background 0.3s;
}

.switch-thumb {
  width: 18px;
  height: 18px;
  background: var(--color-background);
  border-radius: 50%;
  position: absolute;
  left: 0.5px;
  transition: left 0.25s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s;
}

.switch-thumb.dark {
  left: 30px; /* 移到右邊 */
  background: #FAA634; /* 右邊可換顏色，像黃色太陽 */
}

.switch-label {
  width: 60px;
  font-size: 14px;
  color: var(--color-text-2);
}


@media (min-width: 1024px) {
  nav a .icon {
  width: 18px;   /* 控制 icon 大小 */
  height: 18px;
}

  .logo {
    margin: 0 2rem 0 0;
  }

  .nav-top-wrapper {
    width: 100%
  }

  nav {
    text-align: left;
    font-size: 1rem;
  }
}

/* 漢堡選單樣式 */
.hamburger {
  display: none; /* 預設大螢幕隱藏 */
  flex-direction: column;
  gap: 4px;
  width: 25px;
  height: 20px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.hamburger span {
  display: block;
  height: 3px;
  background: var(--color-text-2);
  border-radius: 2px;
  transition: 0.3s;
}

.hamburger span.open:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}
.hamburger span.open:nth-child(2) {
  opacity: 0;
}
.hamburger span.open:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

/* 手機下拉 nav */
nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: max-height 0.3s ease-in-out;
}

nav.open {
  max-height: 500px; /* 足夠內容高度 */
}

@media (max-width: 1023px) {
  header {
    border-bottom: 1px solid var(--color-background-highlight-2);
  }
  
  header .wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  nav {
    max-height: 0;
    overflow: hidden;
  }

  .nav-top {
    justify-content: left;
    gap: 1rem;
    margin: 0;
  }

  .hamburger {
    margin-top: 6px;
    display: flex;
  }

  .nav-top-wrapper {
    width: auto;
  }

  nav a {
    padding: 0.8rem 1rem;
    background: var(--color-background-soft);
    border-radius: 8px;
    margin: 0.3rem 0;
  }
}
</style>
