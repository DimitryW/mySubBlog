<template>
  <div class="success-page">
    <h2>Subscription updated successfully!</h2>
    <router-link to="/subscription">Back to My Subscription</router-link>
  </div>
</template>

<style scoped>
.success-page {
  height: 100vh;              /* 讓容器滿整個視窗高度 */
  font-size: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;         /* 水平方向置中 */
  justify-content: center;     /* 垂直方向置中 */
  gap: 2rem;
  color: var(--color-text-1);
}

.success-page a {
  font-size: 1.2rem;
  text-decoration: underline;
  color: var(--color-text-1);
}

</style>
