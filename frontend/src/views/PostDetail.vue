<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchPost } from '@/api/postService'

const route = useRoute()
const post = ref(null)

onMounted(async () => {
  const response = await fetchPost(route.params.id)
  post.value = response.data
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
      <br/>
      <p v-html=post.body></p>
      <img v-if="post.image" :src="post.image" alt="post image" style="max-width: 300px">
    </div>
  </div>
  <div v-else>
    Loading...
  </div>
</template>

<style scoped>
.post {
  width: 90%;
  margin: 0 auto;
}
</style>
