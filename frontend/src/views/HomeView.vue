<script setup>
import { ref, onMounted } from 'vue'
import { fetchPosts } from '../api/postService.js'

const posts = ref([])

onMounted(async () => {
  try {
    const response = await fetchPosts()
    posts.value = response.data
  } catch (err) {
    console.error(err)
  }
})
</script>

<template>
  <div>
    <h1>Blog Posts</h1>
    <ul>
      <li v-for="post in posts" :key="post.id">
        <h2>{{ post.title }}</h2>
        <p v-html="post.short_body"></p>
        <img v-if="post.image" :src="post.image" alt="post image" style="max-width: 300px">
      </li>
    </ul>
  </div>
</template>
