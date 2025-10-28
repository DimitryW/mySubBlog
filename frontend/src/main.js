// main.js 
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import 'prismjs';
import 'prism-themes/themes/prism-vsc-dark-plus.css'; // 主題
import 'prismjs/components/prism-python'; 
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-bash';


export const prism = {
  mounted(el) {
    Prism.highlightAllUnder(el)
  },
  updated(el) {
    Prism.highlightAllUnder(el)
  }
}

const app = createApp(App)
app.directive('prism', prism)
app.use(createPinia())
app.use(router)
app.mount('#app')
