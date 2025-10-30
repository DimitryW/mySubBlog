<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { fetchMyTransactions } from '@/api/subscription.js'

const userStore = useUserStore()
const transactions = ref([])  // 存交易資料

onMounted(async () => {
  try {
    const data = await fetchMyTransactions()
    transactions.value = data
  } catch (err) {
    console.error('Failed to fetch transactions:', err)
  }
})

const formatDate = (dateString) => {
    if (!dateString) return
  const d = new Date(dateString)
  const pad = (n) => n.toString().padStart(2, '0')
  return `${d.getFullYear()}/${pad(d.getMonth()+1)}/${pad(d.getDate())} ` +
         `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}
</script>

<template>
  <div>
        <div class="table-wrapper" v-if="transactions.length">
            <table>
                <thead>
                <tr>
                    <!-- <th>ID</th> -->
                    <th>Type</th>
                    <th>Amount</th>
                    <th>Payment Method</th>
                    <th>Status</th>
                    <th>Date</th>
                </tr>
                </thead>

                <tbody>
                <tr v-for="tx in transactions" :key="tx.id">
                    <!-- <td>{{ tx.id.slice(-6) }}</td> -->
                    <td>{{ tx.type }}</td>
                    <td class="amount">{{ tx.payment_amount.toFixed(2) }}</td>
                    <td>{{ tx.method }}</td>
                    <td>{{ tx.status }}</td>
                    <td>{{ formatDate(tx.date_paid) }}</td>
                </tr>
                </tbody>
            </table>
        </div>

        <p v-else>No transactions found.</p>
  </div>
</template>

<style scoped>
h2 {
    color: var(--color-text-3);
}

.transaction-history {
  padding: 1rem;
}

/* 手機可以水平滑動 */
.table-wrapper {
  overflow-x: auto;
}

/* 表格樣式 */
table {
  width: 95%;
  border-collapse: collapse;
  min-width: 600px; /* 確保手機滑動時不會太窄 */
  margin: 0 1rem 2rem;
  color: var(--color-text-3);
}

th, td {
  border: 1px solid var(--color-background-highlight-2);
  padding: 0.5rem 0.75rem;
  text-align: left;
  color: var(--color-text-3);
}

th {
  background-color: var(--color-background-highlight-1);
  font-weight: bold;
}

.amount {
    text-align: right;
}
</style>