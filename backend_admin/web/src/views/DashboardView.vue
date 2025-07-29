<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">主控面板</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="handleLogout"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600"
            >
              退出登录
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- 欢迎信息 -->
        <div class="mb-8">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">欢迎使用后台管理系统</h2>
          <p class="text-lg text-gray-600 dark:text-gray-300">请选择要管理的功能模块</p>
        </div>

        <!-- 功能模块网格 -->
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <!-- 图片文件管理 -->
          <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">图片文件管理</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">上传、预览、删除图片文件</p>
                </div>
              </div>
              <div class="mt-4">
                <router-link
                  to="/user-manage"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition-colors duration-200"
                >
                  进入管理
                </router-link>
              </div>
            </div>
          </div>

          <!-- 轮播图管理 -->
          <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h8"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v8"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">轮播图管理</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">管理首页轮播图展示</p>
                </div>
              </div>
              <div class="mt-4">
                <router-link
                  to="/swiper-manage"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 transition-colors duration-200"
                >
                  进入管理
                </router-link>
              </div>
            </div>
          </div>

          <!-- 电话号码管理 -->
          <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">电话号码管理</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">管理联系电话设置</p>
                </div>
              </div>
              <div class="mt-4">
                <router-link
                  to="/phone-manage"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-orange-600 hover:bg-orange-700 dark:bg-orange-500 dark:hover:bg-orange-600 transition-colors duration-200"
                >
                  进入管理
                </router-link>
              </div>
            </div>
          </div>

          <!-- 关于我们管理 -->
          <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-teal-500 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">关于我们管理</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">管理公司介绍和内容</p>
                </div>
              </div>
              <div class="mt-4">
                <router-link
                  to="/about-manage"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-teal-600 hover:bg-teal-700 dark:bg-teal-500 dark:hover:bg-teal-600 transition-colors duration-200"
                >
                  进入管理
                </router-link>
              </div>
            </div>
          </div>

          <!-- 产品管理 -->
          <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-indigo-500 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">产品管理</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">管理产品分类与信息</p>
                </div>
              </div>
              <div class="mt-4">
                <router-link
                  to="/product-manage"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 transition-colors duration-200"
                >
                  进入管理
                </router-link>
              </div>
            </div>
          </div>

          <!-- 企业内容管理 -->
          <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-indigo-500 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5a2 2 0 00-.586-1.414l-4.5-4.5A2 2 0 0012.586 3H9a2 2 0 00-2 2v1m12 13a2 2 0 01-2-2V7m2 13h-3"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">企业内容管理</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">管理企业近期内容展示</p>
                </div>
              </div>
              <div class="mt-4">
                <router-link
                  to="/content-manage"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 transition-colors duration-200"
                >
                  进入管理
                </router-link>
              </div>
            </div>
          </div>

          <!-- 系统设置 -->
          <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-300">
            <div class="p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">系统设置</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">系统配置和用户管理</p>
                </div>
              </div>
              <div class="mt-4">
                <router-link
                  to="/theme-settings"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 transition-colors duration-200"
                >
                  进入设置
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 系统信息 -->
        <div class="mt-8 bg-white dark:bg-gray-800 shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">系统信息</h3>
          </div>
          <div class="px-6 py-4">
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div class="flex justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400">当前用户:</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ user?.username }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400">用户角色:</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">管理员</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400">登录时间:</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ loginTime }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400">系统状态:</span>
                <span 
                  class="text-sm font-medium"
                  :class="{
                    'text-green-600 dark:text-green-400': systemStatus.status === 'running',
                    'text-red-600 dark:text-red-400': systemStatus.status === 'error',
                    'text-yellow-600 dark:text-yellow-400': systemStatus.status === 'warning'
                  }"
                >
                  {{ systemStatus.message }}
                </span>
              </div>
            </div>
            <!-- 系统详细信息 -->
            <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">API版本:</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ systemStatus.version || '未知' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">最后更新:</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ systemStatus.lastUpdate || '未知' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-600 dark:text-gray-400">响应时间:</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ systemStatus.responseTime || '未知' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { config } from '../config/env'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const user = ref(null)
const loginTime = ref('')
const systemStatus = ref({
  status: 'loading',
  message: '检查中...',
  version: '',
  lastUpdate: '',
  responseTime: ''
})

let statusInterval = null

// 获取系统状态
const getSystemStatus = async () => {
  try {
    const startTime = Date.now()
    const response = await fetch(`${config.API_BASE_URL}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.SECRET_KEY}`
      }
    })
    
    const endTime = Date.now()
    const responseTime = endTime - startTime
    
    if (response.ok) {
      const data = await response.json()
      systemStatus.value = {
        status: 'running',
        message: '正常运行',
        version: data.version || '1.0.0',
        lastUpdate: new Date().toLocaleString(),
        responseTime: `${responseTime}ms`
      }
    } else {
      systemStatus.value = {
        status: 'error',
        message: '连接异常',
        version: '',
        lastUpdate: new Date().toLocaleString(),
        responseTime: `${responseTime}ms`
      }
    }
  } catch (error) {
    console.error('获取系统状态失败:', error)
    systemStatus.value = {
      status: 'error',
      message: '网络错误',
      version: '',
      lastUpdate: new Date().toLocaleString(),
      responseTime: '超时'
    }
  }
}

// 获取用户信息
const getUserInfo = async () => {
  try {
    const userInfo = await authStore.getUserInfo()
    user.value = userInfo
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 退出登录
const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}

// 开始自动更新系统状态
const startStatusUpdate = () => {
  // 立即获取一次状态
  getSystemStatus()
  
  // 每30秒自动更新一次状态
  statusInterval = setInterval(() => {
    getSystemStatus()
  }, 300000)
}

// 停止自动更新
const stopStatusUpdate = () => {
  if (statusInterval) {
    clearInterval(statusInterval)
    statusInterval = null
  }
}

// 组件挂载时获取数据
onMounted(async () => {
  await getUserInfo()
  loginTime.value = new Date().toLocaleString()
  startStatusUpdate()
})

// 组件卸载时清理定时器
onUnmounted(() => {
  stopStatusUpdate()
})
</script> 