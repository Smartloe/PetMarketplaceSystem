import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// 端口与代理沿用迁移前 Vue CLI 的约定：开发服务 8010，/api 代理到 Django 8000。
export default defineConfig({
  plugins: [
    vue(),
    // Element Plus 按需引入：模板里的 el-* 组件（含各自样式）按用到的
    // 组件自动注册；JS API 组件（ElMessage / ElMessageBox）不经模板，
    // 其样式在 main.js 手动引入。
    Components({ resolvers: [ElementPlusResolver()] }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 8010,
    open: false,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'static',
  },
})
