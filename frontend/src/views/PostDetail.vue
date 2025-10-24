<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchPost } from '@/api/postService'
import { fetchComments, addComment } from '@/api/commentService'
import { MessageCircle, CornerDownRight } from 'lucide-vue-next'
import Prism from 'prismjs'

const API_BASE = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const router = useRouter()
const post = ref(null)
const notLoggedIn = ref(false)
const contentRef = ref(null)
const comments = ref([])
const newComment = ref('')
const replyContent = ref({})

onMounted(async () => {
  try {
    const res = await fetchPost(route.params.id)
    console.log(res)
    post.value = res.data
    await nextTick()
    if (contentRef.value) {
      Prism.highlightAllUnder(contentRef.value)
    }
    await loadComments()
  } catch (err) {
    if (err.response && [401, 403].includes(err.response.status)) {
      notLoggedIn.value = true
    } else {
      alert('載入失敗或文章不存在')
    }
  }
})

async function loadComments() {
  const res = await fetchComments(route.params.id)
  console.log("comment: ", res)
  comments.value = res.data.results
}

async function submitComment() {
  if (!newComment.value.trim()) return
  await addComment(route.params.id, newComment.value)
  newComment.value = ''
  await loadComments() // 重新載入留言
}

async function submitReply(parentId) {
  if (!replyContent.value[parentId]?.trim()) return
  await addComment(route.params.id, replyContent.value[parentId], parentId)
  replyContent.value[parentId] = ''
  await loadComments()
}

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

const commentSectionRef = ref(null)

function scrollToComments() {
  nextTick(() => {
    if (commentSectionRef.value) {
      commentSectionRef.value.scrollIntoView({ behavior: "smooth" })
    }
  })
}
</script>

<template>
  <div class="posts-wrapper">
  <a @click.prevent="router.back()" class="back-link">← 返回</a>
  <div v-if="post">
    <div class="post">
      <div class="title">
        <h1>{{ post.title }}</h1>
        <div class="post-icon" @click="scrollToComments">
          <MessageCircle class="icon"/>
          <p>{{ post.comments_count }}</p>
        </div>
      </div>
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

  <div ref="commentSectionRef">
    <div v-for="c in comments" :key="c.id" class="comments-section">
      <div>
        <div class="comment-user">{{ c.user }}留言：</div>
        <div class="comment-time">{{ toDateTimeStr(c.created_at) }}</div>
      </div>
      <div>
        {{ c.content }}
      </div>
      <div class="replies">
        <div v-for="r in c.replies" :key="r.id">
          <div class="reply-section">
            <div>
            <p class="reply-user"><CornerDownRight class="icon"/>{{ r.user }}回覆：</p>
            <p class="reply-time">{{ toDateTimeStr(r.created_at) }}</p>
            </div>
            <div class="reply-content">{{ r.content }}</div>
          </div>
          
        </div>
      </div>
      <div v-if="!notLoggedIn" class="reply-form">
        <textarea v-model="replyContent[c.id]" placeholder="回覆..." />
        <button @click="submitReply(c.id)">回覆</button>
      </div>
    </div>

    <div>
      <div v-if="!notLoggedIn" class="comment-form">
        <textarea
          id="comment-content"
          name="comment"
          v-model="newComment"
          placeholder="寫下你的留言..."
        ></textarea>
        <button :disabled="!newComment.trim()" @click="submitComment">送出</button>
      </div>
      <div v-else>
        <p>登入後即可留言。</p>
      </div>
    </div>
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

.title {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.comments-section {
  display: grid;
  grid-template-rows: 1fr 1fr;
  width: 80%;
  margin: 2rem auto;
  color: var(--color-text-1);
  box-shadow: 0 10px 10px 5px rgba(0, 0, 0, 0.1);
  padding: 2rem 3rem;
  border-radius: 8px;
  background: var(--color-background-strong);
}


.comments-section div {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-user {
  font-size: 1.5rem;
  color: var(--color-text-1);
}

.comment-time {
  font-size: 1rem;
  color: var(--color-text-2);
}

.comment-form {
  display: grid;
  grid-template-columns: 11fr 1fr;
  gap: 1rem;
  width: 80%;
  margin: 2rem auto;
  color: var(--color-text-1);
  box-shadow: 0 10px 10px 5px rgba(0, 0, 0, 0.1);
  padding: 2rem 3rem;
  border-radius: 8px;
  background: var(--color-background-strong);
}

.reply-form {
  display: grid !important;
  grid-template-columns: 11fr 1fr;
  gap: 1rem;
  width: 100%;
  margin: 1rem;
  color: var(--color-text-1);
  align-items: start !important;
}

.reply-section {
  display: grid !important;
  grid-template-columns: 1fr;
  width: 100%;
  margin: 1rem 0;
  padding: 0.5rem 0;
  border-top: 1px solid var(--color-background-highlight-2);
}

.reply-user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
}

.reply-time {
  color: var(--color-text-2);
}

.reply-content {
  word-break: break-word;
  white-space: normal;
} 

.comment-form textarea, .reply-form textarea {
  width: 100%;
  border: 1px solid var(--color-background-highlight-2);
  border-radius: 8px;
  padding: 1rem;
  color: var(--color-text-1);
  background: var(--color-background);
}

.comment-form textarea {
  height: 200px;
}

.reply-form textarea {
  height: 60px;
}

.comment-form textarea:focus {
  border: 2px solid var(--color-background-highlight-1);    
  outline: none;  
}

.comment-form button, .reply-form button {
  height: 30px;
  border: none;
  background: var(--color-background-highlight-1);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
}

.replies, reply-form {
  display: block !important;
  padding-left: 1rem;
  margin-top: 0.5rem;
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
  .post, .comments-section, .comment-form {
    width: 100%;
    border-radius: 0;
  }
}

</style>
