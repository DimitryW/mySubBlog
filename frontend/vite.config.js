import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: true, // 允許外部連線
    port: 5173, // 你的 dev server port
    strictPort: true,
    allowedHosts: [
      '2c3f8e6171ad.ngrok-free.app', // 你的 ngrok URL
      '.ngrok-free.app'               // 或允許所有 ngrok 子域名
    ]
  }
})
