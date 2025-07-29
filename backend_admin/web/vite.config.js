import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(),'')
  
  return {
  
    envPrefix: 'APP_',  // 或者设置其他前缀，如 'APP_'
    plugins: [
      tailwindcss(),
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      proxy: {
        '/backend': {
            // target: 'http://111.230.116.93:13286',
        //   target: 'https://api.jeremy233.club',
          target: 'http://localhost:13286',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/backend/, '')
        }
      }
    }
  }
})
