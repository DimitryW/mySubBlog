<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { Home, Info } from 'lucide-vue-next'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">
          <Home class="icon" /> Home
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
  background: #2a2a2a;
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

/* active 狀態 */
nav a.router-link-exact-active {
  background: #424242ff;   /* 淺灰底色 */
  color: #fff;             /* 白字 */
  border-radius: 10px;      /* 圓角邊邊 */
  font-weight: 500;
}

nav a {
  display: flex;
  align-items: center; 
  gap: 0.5rem; 
  padding: 1rem;
  margin: 1rem;
  /* border-left: 1px solid var(--color-border); */
}

/* hover 效果 */
nav a:hover {
  background: #424242ff;   /* 淺灰底色 */
  border-radius: 10px;      /* 圓角邊邊 */
}


@media (min-width: 1024px) {
  header {
    display: block;
    /* place-items: center; */
    /* padding-right: calc(var(--section-gap) / 8); */
    padding-left: calc(var(--section-gap) / 8);
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
