import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import PostDetail from '@/views/PostDetail.vue'
import SubscriptionView from '@/views/SubscriptionView.vue'
import SubscriptionSuccess from '@/views/SubscriptionSuccess.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', name: 'home', component: HomeView},
    {path: '/about', name: 'about', component: AboutView},
    {path: '/posts/:id', name: 'post-detail', component: PostDetail},
    {path: '/subscription', name: 'subscription', component: SubscriptionView},
    {path: '/subscription-success', name: 'subscription-success', component: SubscriptionSuccess},
  ],
})

export default router
