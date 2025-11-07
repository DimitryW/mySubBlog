<script setup>
import { ref, onMounted } from 'vue'
import { getCategories } from '@/api/category'

const categories = ref([])

onMounted(async () => {
    try {
        const res = await getCategories()
        if (res && res.length > 0) {
        categories.value = res
        }
    } catch (err) {
        categories.value = []
    }
})

</script>

<template>
    <div>
    <h1>All Categories</h1>
    <hr />
    <div v-if="categories.length > 0">
        <div class="category-list">
        <RouterLink v-for="t in categories" :key="t.id" :to="`/categories/${t.slug}`" class="category">
        {{ t.name }}({{t.posts_count}})
        </RouterLink>
        </div>
    </div>
    <div v-else class="category-list">
        尚無分類
    </div>
    </div>
</template>

<style scoped>
h1 {
  color: var(--color-text-2);
  height: 100px;
  width: 80%;
  font-weight: 600;
  margin: 0 auto;
  line-height: 100px;
}

hr {
  width: 80%;
  border: 0; 
  border-top: 1px solid var(--color-background-highlight-3); 
  margin: 0 auto 1rem;
  }

.category-list {
  display: flex;           /* 啟用 flex 排列 */
  flex-wrap: wrap;         /* 換行 */
  gap: 12px;               /* 每個 category 之間間距 */
  justify-content: flex-start; /* 左對齊，也可以改 center / space-between */
  width: 80%;
  margin: 0 auto;
  /* box-shadow: 0 2px 6px rgba(0,0,0,0.1); */
}

.category {
  color: var(--color-text-3);
  border-radius: 8px;
  font-weight: 500;
  text-decoration: underline; 
  font-size: 1rem;
}
</style>