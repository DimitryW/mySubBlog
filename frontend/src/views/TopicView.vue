<script setup>
import { ref, onMounted } from 'vue'
import { getTopics } from '@/api/topics'

const topics = ref([])

onMounted(async () => {
    try {
        const res = await getTopics()
        console.log(res);
        if (res && res.length > 0) {
        topics.value = res
        }
    } catch (err) {
        topics.value = []
    }
})

</script>

<template>
    <div>
    <h1>All Topics</h1>
    <div v-if="topics.length > 0">
        <div class="topic-list">
        <div  class="topic" v-for="t in topics" :key="t.id">{{ t.name }}</div>
        </div>
    </div>
    <div v-else>
        尚無分類
    </div>
    </div>
</template>

<style scoped>
h1 {
  color: var(--color-text-1);
  height: 100px;
  width: 80%;
  margin: 0 auto;
  line-height: 100px;
}

.topic-list {
  display: flex;           /* 啟用 flex 排列 */
  flex-wrap: wrap;         /* 換行 */
  gap: 12px;               /* 每個 topic 之間間距 */
  justify-content: flex-start; /* 左對齊，也可以改 center / space-between */
  width: 80%;
  margin: 0 auto;
}

.topic {
  color: var(--color-text-1);
  background-color: var(--color-background-highlight-1); 
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 500;
}
</style>