<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Toast 提示 -->
    <Toast
      :show="showToast"
      :title="toastTitle"
      :message="toastMessage"
      :type="toastType"
      @close="showToast = false"
    />
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button
              @click="goBack"
              class="mr-4 p-2 text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100 transition-colors cursor-pointer"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">主题设置</h1>
          </div>
          <div class="flex items-center space-x-4">
            <!-- 主题选择后自动保存，无需手动保存按钮 -->
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- 设置说明 -->
        <div class="mb-8">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">主题设置</h2>
          <p class="text-lg text-gray-600 dark:text-gray-300">选择您喜欢的主题模式，让界面更符合您的使用习惯</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- 左侧：主题选择面板 -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">主题模式</h3>
            
            <!-- 浅色主题 -->
            <div class="mb-6">
              <div 
                class="border-2 rounded-lg p-4 cursor-pointer transition-all"
                :class="currentTheme === 'light' ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'"
                @click="selectTheme('light')"
              >
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center space-x-3">
                    <div class="w-6 h-6 rounded-full bg-yellow-400 flex items-center justify-center">
                      <svg class="w-4 h-4 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
                      </svg>
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900 dark:text-white">浅色主题</h4>
                      <p class="text-sm text-gray-500 dark:text-gray-400">明亮清晰的界面，适合白天使用</p>
                    </div>
                  </div>
                  <div v-if="currentTheme === 'light'" class="w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center">
                    <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                  </div>
                </div>
                <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded p-3">
                  <div class="flex items-center justify-between mb-2">
                    <div class="w-3 h-3 bg-gray-300 dark:bg-gray-600 rounded"></div>
                    <div class="w-3 h-3 bg-gray-300 dark:bg-gray-600 rounded"></div>
                    <div class="w-3 h-3 bg-gray-300 dark:bg-gray-600 rounded"></div>
                  </div>
                  <div class="space-y-2">
                    <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded"></div>
                    <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                    <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 深色主题 -->
            <div class="mb-6">
              <div 
                class="border-2 rounded-lg p-4 cursor-pointer transition-all"
                :class="currentTheme === 'dark' ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'"
                @click="selectTheme('dark')"
              >
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center space-x-3">
                    <div class="w-6 h-6 rounded-full bg-gray-700 dark:bg-gray-600 flex items-center justify-center">
                      <svg class="w-4 h-4 text-gray-300 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                      </svg>
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900 dark:text-white">深色主题</h4>
                      <p class="text-sm text-gray-500 dark:text-gray-400">护眼舒适的界面，适合夜间使用</p>
                    </div>
                  </div>
                  <div v-if="currentTheme === 'dark'" class="w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center">
                    <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                  </div>
                </div>
                <div class="bg-gray-800 dark:bg-gray-900 border border-gray-600 dark:border-gray-500 rounded p-3">
                  <div class="flex items-center justify-between mb-2">
                    <div class="w-3 h-3 bg-gray-600 dark:bg-gray-500 rounded"></div>
                    <div class="w-3 h-3 bg-gray-600 dark:bg-gray-500 rounded"></div>
                    <div class="w-3 h-3 bg-gray-600 dark:bg-gray-500 rounded"></div>
                  </div>
                  <div class="space-y-2">
                    <div class="h-2 bg-gray-700 dark:bg-gray-600 rounded"></div>
                    <div class="h-2 bg-gray-700 dark:bg-gray-600 rounded w-3/4"></div>
                    <div class="h-2 bg-gray-700 dark:bg-gray-600 rounded w-1/2"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 自动切换说明 -->
            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <div class="flex items-start space-x-3">
                <svg class="w-5 h-5 text-blue-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                </svg>
                <div>
                  <h4 class="text-sm font-medium text-blue-900 dark:text-blue-100">主题切换</h4>
                  <p class="text-sm text-blue-700 dark:text-blue-300 mt-1">选择主题后，系统将自动保存并应用新的主题设置。您可以在任何时候切换主题模式。</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧：小程序二维码设置 -->
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">小程序二维码设置</h3>
            


            <!-- 图片选择 -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">选择小程序二维码图片</label>
              <ImageSelector
                v-model="qrCodeImage"
                v-model:title="qrCodeTitle"
                :multiple="false"
              />
              <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
                请从已上传的图片中选择小程序二维码图片
              </p>
            </div>

            <!-- 配置选项 -->
            <div class="mb-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">二维码标题</label>
                <input
                  v-model="qrCodeTitle"
                  type="text"
                  class="block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  placeholder="小程序二维码"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">二维码描述</label>
                <textarea
                  v-model="qrCodeDescription"
                  rows="3"
                  class="block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  placeholder="扫描二维码体验小程序"
                ></textarea>
              </div>
              
              <div class="flex items-center">
                <input
                  v-model="qrCodeEnabled"
                  type="checkbox"
                  id="qr-code-enabled"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded dark:border-gray-600 dark:bg-gray-800"
                />
                <label for="qr-code-enabled" class="ml-2 block text-sm text-gray-900 dark:text-gray-100">
                  启用小程序二维码显示
                </label>
              </div>
            </div>

            <!-- 保存按钮 -->
            <div class="flex justify-end">
              <button
                @click="saveQrCodeSettings"
                :disabled="loading"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                {{ loading ? '保存中...' : '保存二维码设置' }}
              </button>
            </div>

            <!-- 说明 -->
            <div class="mt-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
              <div class="flex items-start space-x-3">
                <svg class="w-5 h-5 text-yellow-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                </svg>
                <div>
                  <h4 class="text-sm font-medium text-yellow-900 dark:text-yellow-100">二维码设置说明</h4>
                  <p class="text-sm text-yellow-700 dark:text-yellow-300 mt-1">设置的小程序二维码将在首页展示，建议使用清晰的二维码图片，大小建议为200x200像素以上。请先在用户管理页面上传图片，然后在此处选择。配置将保存到服务器的配置文件中。</p>
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
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '../stores/theme'
import { useAuthStore } from '../stores/auth'
import Toast from '../components/Toast.vue'
import ImageSelector from '../components/ImageSelector.vue'

const router = useRouter()
const themeStore = useThemeStore()
const authStore = useAuthStore()

// Toast 提示状态
const showToast = ref(false)
const toastTitle = ref('')
const toastMessage = ref('')
const toastType = ref('info')

// 当前主题
const currentTheme = ref('light')

// 小程序二维码设置
const qrCodeImage = ref('')
const qrCodeTitle = ref('')
const qrCodeDescription = ref('')
const qrCodeEnabled = ref(false)
const loading = ref(false)

// 监听二维码图片变化
watch(qrCodeImage, (newValue) => {
  if (newValue) {
    handleQrCodeImageChange()
  }
})

// 显示Toast提示
const showToastMessage = (title, message = '', type = 'info') => {
  toastTitle.value = title
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
}

// 选择主题
const selectTheme = (theme) => {
  currentTheme.value = theme
  themeStore.setTheme(theme)
  // 选择主题后直接保存
  if (themeStore.saveThemeSettings()) {
    showToastMessage('主题已切换', `已切换到${theme === 'light' ? '浅色' : '深色'}主题`, 'success')
  } else {
    showToastMessage('保存失败', '主题设置保存失败，请重试', 'error')
  }
}

// 加载小程序二维码配置
const loadQrCodeConfig = async () => {
  try {
    loading.value = true
    const response = await authStore.authenticatedFetch('/api/qr-code/config')
    
    if (response.ok) {
      const result = await response.json()
      if (result.success) {
        const data = result.data
        qrCodeImage.value = data.image || ''
        qrCodeTitle.value = data.title || '小程序二维码'
        qrCodeDescription.value = data.description || '扫描二维码体验小程序'
        qrCodeEnabled.value = data.enabled || false
      }
    } else {
      showToastMessage('加载失败', '获取小程序二维码配置失败', 'error')
    }
  } catch (error) {
    console.error('加载小程序二维码配置失败:', error)
    showToastMessage('加载失败', '网络错误，请重试', 'error')
  } finally {
    loading.value = false
  }
}

// 监听二维码图片选择变化
const handleQrCodeImageChange = async () => {
  if (qrCodeImage.value) {
    // 当选择了图片时，自动启用二维码并保存配置
    await saveQrCodeSettings()
    showToastMessage('选择成功', '小程序二维码图片已选择并保存', 'success')
  }
}





// 保存二维码设置
const saveQrCodeSettings = async () => {
  try {
    loading.value = true
    const response = await authStore.authenticatedFetch('/api/qr-code/config', {
      method: 'PUT',
      body: JSON.stringify({
        image: qrCodeImage.value,
        title: qrCodeTitle.value,
        description: qrCodeDescription.value,
        enabled: qrCodeEnabled.value
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      if (result.success) {
        showToastMessage('保存成功', '小程序二维码配置已保存到服务器', 'success')
        // 重新加载配置
        await loadQrCodeConfig()
      } else {
        showToastMessage('保存失败', result.message || '保存失败', 'error')
      }
    } else {
      showToastMessage('保存失败', '保存小程序二维码配置失败', 'error')
    }
  } catch (error) {
    console.error('保存小程序二维码配置失败:', error)
    showToastMessage('保存失败', '网络错误，请重试', 'error')
  } finally {
    loading.value = false
  }
}

// 返回上一页
const goBack = () => {
  router.go(-1)
}

// 组件挂载时初始化
onMounted(async () => {
  // 加载保存的主题设置
  themeStore.loadThemeSettings()
  // 直接从 localStorage 读取主题设置，确保获取到正确的值
  try {
    const savedTheme = localStorage.getItem('currentTheme')
    if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
      currentTheme.value = savedTheme
    } else {
      currentTheme.value = 'light'
    }
  } catch (error) {
    console.error('读取主题设置失败:', error)
    currentTheme.value = 'light'
  }

  // 加载小程序二维码配置
  await loadQrCodeConfig()
})
</script>

<style scoped>
/* 自定义样式 */
.theme-preview {
  transition: all 0.3s ease;
}
</style> 