<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getImageUrlWithToken } from '../config/env'

// 轮播图数据
const swiperList = ref([])

// 认证store
const authStore = useAuthStore()

// 小程序二维码数据
const qrCodeImage = ref('')
const qrCodeTitle = ref('')
const qrCodeDescription = ref('')
const qrCodeEnabled = ref(false)

// 功能特性数据
const features = ref([
  {
    icon: '🎯',
    title: '智能内容管理',
    description: '一键轮播图管理、产品展示系统、企业形象塑造、品牌信息维护',
    color: 'bg-blue-500'
  },
  {
    icon: '🔐',
    title: '企业级安全认证',
    description: '双重登录保障、JWT安全令牌、权限精细控制',
    color: 'bg-green-500'
  },
  {
    icon: '📊',
    title: '智能文件管理',
    description: '海量图片处理、智能预览系统、分组管理',
    color: 'bg-purple-500'
  },
  {
    icon: '🎨',
    title: '现代化用户体验',
    description: '响应式设计、主题切换、实时反馈、直观导航',
    color: 'bg-orange-500'
  },
  {
    icon: '⚡',
    title: '高性能架构',
    description: '懒加载优化、分页显示、缓存机制、并发处理',
    color: 'bg-red-500'
  },
  {
    icon: '🏗️',
    title: '现代化技术栈',
    description: 'FastAPI + Vue3 + TailwindCSS，容器化部署',
    color: 'bg-indigo-500'
  }
])

// 系统性能数据
const performanceStats = ref([
  { label: '响应速度', value: '< 100ms', icon: '⚡' },
  { label: '并发支持', value: '100+ 用户', icon: '👥' },
  { label: '图片处理', value: '10MB 以内', icon: '🖼️' },
  { label: '存储优化', value: '节省 50%', icon: '💾' }
])

// 适用场景
const useCases = ref([
  {
    title: '企业官网后台',
    description: '管理企业官网内容、产品信息',
    icon: '🏢'
  },
  {
    title: '电商平台管理',
    description: '产品展示',
    icon: '🛒'
  },
  {
    title: '内容管理系统',
    description: '文章、图片',
    icon: '📝'
  },
  {
    title: '企业形象展示',
    description: '企业介绍、新闻动态、联系方式管理',
    icon: '📊'
  }
])

// 加载小程序二维码配置
const loadQrCodeConfig = async () => {
  try {
    const response = await authStore.authenticatedFetch('/api/qr-code/public')
    if (response.ok) {
      const result = await response.json()
      if (result.success && result.data) {
        qrCodeImage.value = result.data.image
        qrCodeTitle.value = result.data.title
        qrCodeDescription.value = result.data.description
        qrCodeEnabled.value = true
      }
    }
  } catch (error) {
    console.error('加载小程序二维码配置失败:', error)
  }
}

// 组件挂载时初始化
onMounted(() => {
  loadQrCodeConfig()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- 导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm dark:shadow-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">🚀 企业级后台管理系统</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              to="/login"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
            >
              登录
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      
      <!-- 主标题区域 -->
      <div class="text-center">
        <h2 class="text-4xl font-extrabold text-gray-900 dark:text-white sm:text-5xl">
          企业级后台管理系统
        </h2>
        <p class="mt-4 text-xl text-gray-600 dark:text-gray-300">
          一个功能强大、界面精美的现代化企业后台管理系统，专为企业设计
        </p>
        
        <div class="mt-8 flex justify-center space-x-4">
          <router-link
            to="/login"
            class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
          >
            开始使用
          </router-link>
          <a
            href="#features"
            class="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
          >
            了解更多
          </a>
        </div>
      </div>

      <!-- 小程序二维码展示区域 -->
      <div v-if="qrCodeEnabled && qrCodeImage" class="mt-16">
        <div class="text-center mb-8">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white">📱 扫码体验小程序</h3>
          <p class="mt-2 text-lg text-gray-600 dark:text-gray-300">{{ qrCodeDescription }}</p>
        </div>
        
        <div class="flex justify-center">
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg dark:shadow-gray-700 p-8 text-center">
            <div class="mb-4">
              <img
                :src="getImageUrlWithToken(qrCodeImage)"
                :alt="qrCodeTitle"
                class="mx-auto w-48 h-48 object-contain rounded-lg border-2 border-gray-200 dark:border-gray-600"
              />
            </div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {{ qrCodeTitle }}
            </h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              使用微信扫描二维码，即可体验小程序
            </p>
          </div>
        </div>
      </div>

      <!-- 核心功能亮点 -->
      <div id="features" class="mt-20">
        <div class="text-center mb-12">
          <h3 class="text-3xl font-bold text-gray-900 dark:text-white">✨ 核心功能亮点</h3>
          <p class="mt-4 text-lg text-gray-600 dark:text-gray-300">专为企业数字化转型而设计的强大功能</p>
        </div>
        
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div 
            v-for="feature in features" 
            :key="feature.title"
            class="bg-white dark:bg-gray-800 overflow-hidden shadow-lg dark:shadow-gray-700 rounded-xl hover:shadow-xl transition-shadow duration-300"
          >
            <div class="p-6">
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl">
                    {{ feature.icon }}
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {{ feature.title }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                    {{ feature.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 系统性能 -->
      <div class="mt-20">
        <div class="text-center mb-12">
          <h3 class="text-3xl font-bold text-gray-900 dark:text-white">📊 系统性能</h3>
          <p class="mt-4 text-lg text-gray-600 dark:text-gray-300">企业级性能保障，稳定可靠</p>
        </div>
        
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div 
            v-for="stat in performanceStats" 
            :key="stat.label"
            class="bg-white dark:bg-gray-800 rounded-lg shadow-md dark:shadow-gray-700 p-6 text-center"
          >
            <div class="text-3xl mb-2">{{ stat.icon }}</div>
            <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ stat.value }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">{{ stat.label }}</div>
          </div>
        </div>
      </div>

      <!-- 适用场景 -->
      <div class="mt-20">
        <div class="text-center mb-12">
          <h3 class="text-3xl font-bold text-gray-900 dark:text-white">🎯 适用场景</h3>
          <p class="mt-4 text-lg text-gray-600 dark:text-gray-300">满足不同企业的多样化需求</p>
        </div>
        
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div 
            v-for="useCase in useCases" 
            :key="useCase.title"
            class="bg-white dark:bg-gray-800 rounded-lg shadow-md dark:shadow-gray-700 p-6 text-center hover:shadow-lg transition-shadow duration-300"
          >
            <div class="text-4xl mb-4">{{ useCase.icon }}</div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {{ useCase.title }}
            </h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              {{ useCase.description }}
            </p>
          </div>
        </div>
      </div>

      <!-- 技术优势 -->
      <div class="mt-20">
        <div class="text-center mb-12">
          <h3 class="text-3xl font-bold text-gray-900 dark:text-white">🔧 技术优势</h3>
          <p class="mt-4 text-lg text-gray-600 dark:text-gray-300">采用最新技术栈，性能优异</p>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg dark:shadow-gray-700 p-8">
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-gray-900 dark:text-white">现代化架构</span>
            </div>
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-gray-900 dark:text-white">容器化部署</span>
            </div>
            <div class="flex items-center">
              <div class="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-gray-900 dark:text-white">安全可靠</span>
            </div>
            <div class="flex items-center">
              <div class="w-8 h-8 bg-orange-500 rounded-md flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-gray-900 dark:text-white">易于扩展</span>
            </div>
            <div class="flex items-center">
              <div class="w-8 h-8 bg-red-500 rounded-md flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-gray-900 dark:text-white">维护简单</span>
            </div>
        
          </div>
        </div>
      </div>

      <!-- 行动号召 -->
      <div class="mt-20 text-center">
        <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
          <h3 class="text-3xl font-bold mb-4">让企业数字化转型更简单，让内容管理更高效！</h3>
          <p class="text-xl mb-6 opacity-90">立即开始体验企业级后台管理系统的强大功能</p>
          <router-link
            to="/login"
            class="inline-flex items-center px-8 py-4 border-2 border-white text-lg font-medium rounded-lg text-white hover:bg-white hover:text-blue-600 transition-colors duration-300"
          >
            立即开始使用 🚀
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

