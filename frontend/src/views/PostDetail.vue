<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchPost } from '@/api/postService'
import Prism from 'prismjs'

const API_BASE = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()
const post = ref(null)
const notLoggedIn = ref(false)
const contentRef = ref(null)

onMounted(async () => {
  try {
    const res = await fetchPost(route.params.id)
    console.log(res)
    post.value = res.data
    await nextTick()
    if (contentRef.value) {
      Prism.highlightAllUnder(contentRef.value)
    }
  } catch (err) {
    if (err.response && [401, 403].includes(err.response.status)) {
      notLoggedIn.value = true
    } else {
      alert('載入失敗或文章不存在')
    }
  }
})

// 若 post.body 會改變（例如重新載入），再監聽一次
watch(post, async () => {
  await nextTick()
  if (contentRef.value) {
    Prism.highlightAllUnder(contentRef.value)
  }
})

function toDateTimeStr(dateString) {
  const date = new Date(dateString);
  const dateStr = date.toLocaleDateString(navigator.language, {year: 'numeric', month: 'long', day: 'numeric'});
  const timeStr = date.toLocaleTimeString(navigator.language, {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
  return `${dateStr} ${timeStr}`;
}
</script>

<template>
  <div class="posts-wrapper">
  <a @click.prevent="router.back()" class="back-link">← 返回</a>
  <div v-if="post">
    <div class="post">
      <h1>{{ post.title }}</h1>
      <p class="post-time">{{ toDateTimeStr(post.created_at) }}</p>
      <hr/>
      <div class="tag-wrapper">
        <RouterLink v-for="tag in post.tags" :key="tag" :to="`/tags/${tag}`" class="tag">
          #{{ tag }}
        </RouterLink>
      </div>
      <br/>
      <div class="post-body" v-html="post.body" ref="contentRef"></div>
      <img v-if="post.image" :src="post.image" alt="post image" style="max-width: 300px">
    </div>
  </div>
  <div v-else-if="notLoggedIn">
    <p>你尚未登入，請先登入查看文章</p>
    <a :href="`${API_BASE}/accounts/login/`">前往登入</a>
  </div>
  </div>
</template>

<style scoped>
h1 {
  color: var(--color-text-1);
  font-size: 2rem;
  font-weight: 600;
}

hr {
  border: 0; 
  border-top: 1px solid var(--color-background-highlight-3); 
  margin: 0.5rem 0;
  }

.posts-wrapper {
  display: grid;
  grid-template-rows: auto 1fr;
}
.back-link { 
  width: 80%;
  margin: 1rem auto 0;
  text-align: right;
  color: var(--color-text-2); 
  text-decoration: none; cursor: pointer; 
} 
  
.back-link:hover { 
  text-decoration: underline; 
}

.post {
  width: 80%;
  min-height: 800px;
  margin: 2rem auto;
  color: var(--color-text-1);
  box-shadow: 0 10px 10px 5px rgba(0, 0, 0, 0.1);
  padding: 3rem 3rem 5rem;
  border-radius: 8px;
  background: var(--color-background-strong);
}

.post-time {
  color: var(--color-text-2);
}

.posts-wrapper, .post {
  display: flex;
  flex-direction: column;
}
.post-body {
  flex: 1;
  overflow: auto;
}

/* Prism.js 語法區塊 */
.post-body pre {
  background: #2d2d2d;
  color: #ccc;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto; /* 保留水平滾動條 */
  font-family: "Fira Code", monospace;
  white-space: pre-wrap;   /* 允許換行 */
  word-wrap: break-word;   /* 強制長單詞換行 */
  width: 100vw
}

@media (max-width: 1023px) {
  .post {
    width: 100%;
    border-radius: 0;
  }
}

</style>
