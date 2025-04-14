import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
//导入element-plus
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  assetsInclude: ['**/*.PNG'], // 支持 .PNG 文件
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // 您的后端服务器地址
        changeOrigin: true, // 避免在请求头中添加 Host: 127.0.0.1:5000
        rewrite: (path) => path.replace(/^\/api/, ''), // 重写路径，移除 /api 前缀
      },
    },
  },
})
