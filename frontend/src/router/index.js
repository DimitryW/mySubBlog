import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import PostDetail from '@/views/PostDetail.vue'
import SubscriptionView from '@/views/SubscriptionView.vue'
import SubscriptionSuccess from '@/views/SubscriptionSuccess.vue'
import CategoriesView from '@/views/Categories.vue'
import CategoriesPostsView from '@/views/CategoriesPostsView.vue'
import TagPostsView from '@/views/TagPostsView.vue'
import Account from '@/views/AccountView.vue'
import MembersOnlyView from '@/views/MembersOnly.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', name: 'home', component: HomeView},
    {path: '/about', name: 'about', component: AboutView},
    {path: '/posts/:id', name: 'post-detail', component: PostDetail},
    {path: '/subscription', name: 'subscription', component: SubscriptionView},
    {path: '/subscription-success', name: 'subscription-success', component: SubscriptionSuccess},
    {path: '/categories', name: 'categories', component: CategoriesView},
    {path: '/categories/:slug', name: 'CategoryPosts', component: CategoriesPostsView},
    {path: '/tags/:tag', name: 'TagPosts', component: TagPostsView},
    {path: '/account', name: 'account', component: Account},
    {path: '/members', name: 'membersOnly', component: MembersOnlyView},
  ],
})

export default router
