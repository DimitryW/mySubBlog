<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchPost } from '@/api/postService'

const API_BASE = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const post = ref(null)
const notLoggedIn = ref(false)

onMounted(async () => {
  try {
    const res = await fetchPost(route.params.id)
    post.value = res.data
  } catch (err) {
    if (err.response && [401, 403].includes(err.response.status)) {
      notLoggedIn.value = true
    } else {
      alert('載入失敗或文章不存在')
    }
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
  <div v-if="post">
    <div class="post">
      <h1>{{ post.title }}</h1>
      <p>{{ toDateTimeStr(post.created_at) }}</p>
      <div class="tag-wrapper">
        <p class="tag" v-for="tag in post.tags" :key="tag">{{ tag }}</p>
      </div>
      <br/>
      <p v-html="post.body"></p>
      <img v-if="post.image" :src="post.image" alt="post image" style="max-width: 300px">
    </div>
  </div>
  <div v-else-if="notLoggedIn">
    <p>你尚未登入，請先登入查看文章</p>
    <a :href="`${API_BASE}/accounts/login/`">前往登入</a>
  </div>
</template>

<style scoped>
.post {
  width: 90%;
  margin: 0 auto;
  color: var(--color-text-1);
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  padding: 3rem 3rem 5rem;
  margin: 0 2rem;
}

</style>
