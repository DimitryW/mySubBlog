<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MessageCircle, LockKeyhole, LockKeyholeOpen } from 'lucide-vue-next'
import { getCategoriesPosts } from '@/api/category'
import { is_subscribed } from '@/api/accountUsers.js'

const route = useRoute()
const router = useRouter()
const posts = ref([])
const categoryName = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const loading = ref(false)

const loadPosts = async (page = 1) => {
  loading.value = true
  categoryName.value = route.params.slug
  try {
    const res = await getCategoriesPosts(categoryName.value, page)
    console.log(res)
    posts.value = res.results
    currentPage.value = page
    // 計算總頁數
    totalPages.value = Math.ceil(res.count / 10)
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => loadPosts(1))

const prevPage = () => {
  if (currentPage.value > 1) loadPosts(currentPage.value - 1)
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) loadPosts(currentPage.value + 1)
}

function timeAgo(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  const rtf = new Intl.RelativeTimeFormat(navigator.language, { numeric: "auto" })

  if (diffSec < 60) return rtf.format(-diffSec, "second")
  if (diffMin < 60) return rtf.format(-diffMin, "minute")
  if (diffHour < 24) return rtf.format(-diffHour, "hour")
  if (diffDay <= 3) return rtf.format(-diffDay, "day")
  return date.toLocaleDateString(navigator.language, { year: 'numeric', month: 'long', day: 'numeric' })
}
</script>

<template>
  <div class="page-wrapper">
  <div>
    <div class="header"> 
    <h1>Category:&nbsp;<span class="category-name">{{ categoryName }}</span></h1> 
    <a @click.prevent="router.back()" class="back-link">← 返回</a>
    </div>
    <div v-if="posts.length > 0">
    <ul class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <RouterLink :to="`/posts/${post.id}`">
          <div class="title">
            <h2>{{ post.title }}</h2>
            <div v-if="post.is_locked">
              <div v-if="!is_subscribed" class="corner-lock-ribbon">
                <LockKeyhole class="icon-lock" />
                <span>僅限訂閱會員閱讀</span>
              </div>
              <div v-if="is_subscribed" class="corner-unlock-ribbon">
                <LockKeyholeOpen class="icon-lock" />
                <span>訂閱會員限定</span>
              </div>
            </div>
            <div class="post-icon" @click="scrollToComments">
              <MessageCircle class="icon"/>
              <p>{{ post.comments_count }}</p>
            </div>
          </div>
          <p>{{ timeAgo(post.created_at) }}</p>
          <hr/>
          <div class="tag-wrapper">
            <p class="tag" v-for="tag in post.tags" :key="tag">#{{ tag }}</p>
          </div>
          <br/>
          <p v-html="post.short_body"></p>
        </RouterLink>
      </div>
    </ul>
    </div>
    <div v-else class="no-post"> 尚無文章 </div>
  </div>
  
  <div class="pagination">
    <button @click="prevPage" :disabled="currentPage === 1">上一頁</button>
    <span>第 {{ currentPage }} / {{ totalPages }} 頁</span>
    <button @click="nextPage" :disabled="currentPage === totalPages">下一頁</button>
  </div>
  </div> 
</template>

<style scoped>
h2 {
  color: var(--color-text-1);
  font-size: 2rem;
  font-weight: 600;
}

.title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}


.corner-lock-ribbon {
  display: flex;
  gap: 0.3rem;
  align-items: center;
  background: rgba(255, 0, 0, 0.1);
  color: #d00;
  text-align: center;
  font-size: 0.8rem;
  font-weight: bold;
  position: absolute;
  top: 10px;
  right: 0;
  padding: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.corner-unlock-ribbon {
  display: flex;
  gap: 0.3rem;
  align-items: center;
  background: rgb(10 173 0 / 14%);
  color: #1a9000;
  text-align: center;
  font-size: 0.8rem;
  font-weight: bold;
  position: absolute;
  top: 10px;
  right: 0;
  padding: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.post-icon {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  color: var(--color-text-2);
  cursor: pointer;
}

.icon {
  width: 18px;
  height: 18px;
}

hr {
  border: 0; 
  border-top: 1px solid var(--color-background-highlight-3); 
  margin: 0.5rem 0;
  }

.page-wrapper {
  display:grid;
  grid-template-rows: 1fr 4rem;
}
.header { 
  width: 80%;
  display: flex; 
  justify-content: 
  space-between; 
  align-items: center; 
  margin: 0 auto; 
}

h1 {
  color: var(--color-text-2);
  font-weight: 600;
  line-height: 100px;
}

.category-name {
  color: var(--color-text-1);
  font-weight: 600;
}

.back-link { 
  color: var(--color-text-2); 
  text-decoration: none; cursor: pointer; 
} 
  
.back-link:hover { 
  text-decoration: underline; 
}

.no-post {
  width: 80%;
  color: var(--color-text-2);
  margin: 0 auto;
}

.post-list {
  list-style: none;
  padding: 0 0 2rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}
.post-card {
  width: 80%;
  background: var(--color-background-strong);
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  padding: 1rem;
  color: var(--color-text-2);
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  word-wrap: break-word; 
  position: relative;
}
.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.post-card a {
  text-decoration: none;
  color: inherit;
  display: block;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  color: var(--color-text-2);
}

.pagination button{
  background: var(--vt-c-indigo);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
  pointer-events: none;
}
</style>
