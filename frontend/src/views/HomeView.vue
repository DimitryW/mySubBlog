<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { fetchPosts } from '../api/postService.js'

const posts = ref([])
const currentPage = ref(1)
const hasNextPage = ref(false)
const loading = ref(false)

let observer = null
const loadMoreTrigger = ref(null) // 監聽這個元素是否進入視窗

async function loadPosts(page = 1, append = false) {
  if (loading.value) return
  loading.value = true
  try {
    const response = await fetchPosts(page)
    if (append) {
      posts.value.push(...response.data.results)
    } else {
      posts.value = response.data.results
    }
    hasNextPage.value = response.data.next !== null
    currentPage.value = page
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPosts(1).then(() => {
    // 等 DOM 更新完再建立 observer
    nextTick(() => {
      if (!loadMoreTrigger.value) return

      // 建立 IntersectionObserver
      observer = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting && hasNextPage.value && !loading.value) {
            loadPosts(currentPage.value + 1, true)
          }
        },
        { threshold: 0 } 
      )

      observer.observe(loadMoreTrigger.value)

      const rect = loadMoreTrigger.value.getBoundingClientRect()
      if (rect.top < window.innerHeight) {
        if (hasNextPage.value && !loading.value) {
          loadPosts(currentPage.value + 1, true)
        }
      }
    })
  })
})

onUnmounted(() => {
  if (observer && loadMoreTrigger.value) {
    observer.unobserve(loadMoreTrigger.value)
  }
})

function timeAgo(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  const rtf = new Intl.RelativeTimeFormat(navigator.language, { numeric: "auto" });

  let parts;

  if (diffSec < 60) {
    // 少於 1 分鐘
    parts = rtf.formatToParts(-diffSec, "second");
  } else if (diffMin < 60) {
    // 少於 1 小時
    parts = rtf.formatToParts(-diffMin, "minute");
  } else if (diffHour < 24) {
    // 少於 1 天
    parts = rtf.formatToParts(-diffHour, "hour");
  } else if (diffDay <= 3) {
    // 三天內
    parts = rtf.formatToParts(-diffDay, "day");
  } else {
    // 超過三天 → 用日期顯示
    return date.toLocaleDateString(navigator.language,{year: 'numeric', month: 'long', day: 'numeric'});
  }

  // 組合 formatToParts 的結果
  return parts.map(p => p.value).join("");
}
</script>

<template>
  <div>
    <h1>All Posts</h1>
    <ul class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-card">
      <RouterLink :to="`/posts/${post.id}`">
        <h2>{{ post.title }}</h2>
        <p>{{ timeAgo(post.created_at) }}</p>
        <br/>
        <p v-html="post.short_body"></p>
        </RouterLink>
        <!-- <img v-if="post.image" :src="post.image" alt="post image" style="max-width: 300px"> -->
      </div>
    </ul>
    <!-- loading 提示 -->
    <p v-if="loading">Loading...</p>

    <!-- 觸發載入的元素 -->
    <div ref="loadMoreTrigger" style="height: 1px"></div>
  </div>
</template>

<style scoped>
h1 {
  width: 90%;
  margin: 0 auto;
}

h2 {
  color: #fff;
  font-size: 26px;
}

/* 讓 ul 的內容置中排列 */
.post-list {
  list-style: none;
  padding: 0 0 2rem 0;
  display: flex;
  flex-direction: column; /* 垂直排列 */
  align-items: center;   /* 水平置中 */
  gap: 2rem;             /* 卡片間距 */
}

/* 卡片 */
.post-card {
  width: 90%; 
  max-height: 1200px;
  background: #2a2a2a;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  padding: 1rem;
  color: #b1b1b1;
  text-align: left;           /* 卡片內容靠左對齊 */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* hover 效果 */
.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* 讓 RouterLink 填滿卡片 */
.post-card a {
  text-decoration: none;
  color: inherit;
  display: block;
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
