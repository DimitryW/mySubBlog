// main.js 
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import 'prismjs';
import 'prism-themes/themes/prism-vsc-dark-plus.css'; // 主題
import 'prismjs/components/prism-python'; // 載入 Python 語法
import 'prismjs/components/prism-javascript'; // 載入 JavaScript 語法


const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
