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
</script>

<template>
  <div v-if="post">
    <div class="post">
      <h1>{{ post.title }}</h1>
      <p>{{ new Date(post.created_at).toLocaleString() }}</p>
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
