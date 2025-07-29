<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">轮播图管理</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              to="/dashboard"
              class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 text-sm leading-4 font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              返回主控面板
            </router-link>
            <button
              @click="handleLogout"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
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
        <!-- 操作栏 -->
        <div class="mb-6 flex justify-between items-center">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">轮播图配置</h2>
          <div class="flex space-x-3">
            <button
              @click="showCreateModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              添加轮播图
            </button>
            <button
              @click="saveConfig"
              :disabled="saving"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
            >
              <svg v-if="saving" class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path>
              </svg>
              {{ saving ? '保存中...' : '保存配置' }}
            </button>
          </div>
        </div>

        <!-- 轮播图列表 -->
        <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-md">
          <div v-if="swiperList.length === 0" class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">暂无轮播图</h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">开始添加您的第一个轮播图吧。</p>
          </div>
          
          <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="(swiper, index) in swiperList" :key="index" class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <!-- 轮播图预览 -->
                  <div class="flex-shrink-0">
                    <img
                      :src="getPreviewUrl(swiper.image)"
                      :alt="swiper.title"
                      class="h-16 w-24 object-cover rounded-lg"
                    />
                  </div>
                  
                  <!-- 轮播图信息 -->
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {{ swiper.title || '无标题' }}
                    </p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                      {{ swiper.image }}
                    </p>
                    <div class="flex items-center space-x-4 mt-1">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
                        排序: {{ index + 1 }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- 操作按钮 -->
                <div class="flex items-center space-x-2">
                  <button
                    v-if="index > 0"
                    @click="moveSwiper(index, 'up')"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                    </svg>
                  </button>
                  <button
                    v-if="index < swiperList.length - 1"
                    @click="moveSwiper(index, 'down')"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </button>
                  <button
                    @click="editSwiper(index)"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    编辑
                  </button>
                  <button
                    @click="deleteSwiper(index)"
                    class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-red-700 dark:text-red-400 bg-red-100 dark:bg-red-900 hover:bg-red-200 dark:hover:bg-red-800"
                  >
                    删除
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="text-center py-8">
          <div class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            加载中...
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑模态框 -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-transparent   overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-200 shadow-lg rounded-md bg-white dark:bg-gray-800 dark:border-gray-700">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
            {{ showEditModal ? '编辑轮播图' : '添加轮播图' }}
          </h3>
          
          <form @submit.prevent="showEditModal ? updateSwiper() : createSwiper()" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
              <input
                v-model="form.title"
                type="text"
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                placeholder="请输入标题（可选）"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">图片</label>
              <div class="mt-1">
                <!-- 图片选择组件 -->
                <ImageSelector 
                  v-model="form.image" 
                />
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="submitting || !form.image"
                class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
              >
                {{ submitting ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 添加消息提示对话框 -->
    <ConfirmDialog
      v-model:show="showMessageDialog"
      :title="messageDialogConfig.title"
      :message="messageDialogConfig.message"
      :type="messageDialogConfig.type"
      confirmText="确定"
      :showCancel="false"
      @confirm="closeMessageDialog"
      @cancel="closeMessageDialog"
    />

    <!-- 添加确认对话框组件 -->
    <ConfirmDialog
      v-model:show="showDeleteConfirm"
      title="删除确认"
      message="确定要删除这个轮播图吗？"
      type="danger"
      confirmText="删除"
      cancelText="取消"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ImageSelector from '../components/ImageSelector.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'  // 导入 ConfirmDialog 组件
import { getImageUrlWithToken } from '../config/env'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const swiperList = ref([])
const loading = ref(false)
const saving = ref(false)
const submitting = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingIndex = ref(-1)

// 添加删除确认相关的响应式数据
const showDeleteConfirm = ref(false)
const deletingIndex = ref(-1)

// 添加消息提示对话框相关的响应式数据
const showMessageDialog = ref(false)
const messageDialogConfig = ref({
  title: '',
  message: '',
  type: 'info'
})

// 表单数据
const form = ref({
  title: '',
  image: ''
})

// 获取轮播图配置
const getSwiperConfig = async () => {
  loading.value = true
  try {
    const response = await authStore.authenticatedFetch('/api/swiper/config')
    if (response.ok) {
      const data = await response.json()
      swiperList.value = data.images || []
    }
  } catch (error) {
    console.error('获取轮播图配置失败:', error)
  } finally {
    loading.value = false
  }
}

// 显示消息对话框
const showMessage = (title, message, type = 'info') => {
  messageDialogConfig.value = {
    title,
    message,
    type
  }
  showMessageDialog.value = true
}

// 关闭消息对话框
const closeMessageDialog = () => {
  showMessageDialog.value = false
}

// 保存轮播图配置
const saveConfig = async () => {
  saving.value = true
  try {
    const response = await authStore.authenticatedFetch('/api/swiper/config', {
      method: 'PUT',
      body: JSON.stringify({
        images: swiperList.value
      })
    })
    
    if (response.ok) {
      showMessage('成功', '配置保存成功', 'info')
    } else {
      const error = await response.json()
      showMessage('错误', error.detail || '保存失败', 'danger')
    }
  } catch (error) {
    console.error('保存配置失败:', error)
    showMessage('错误', '保存失败', 'danger')
  } finally {
    saving.value = false
  }
}

// 创建轮播图
const createSwiper = async () => {
  if (!form.value.image) {
    showMessage('提示', '请选择图片', 'warning')
    return
  }
  
  submitting.value = true
  try {
    swiperList.value.push({
      title: form.value.title || '',
      image: form.value.image
    })
    
    closeModal()
  } catch (error) {
    console.error('创建轮播图失败:', error)
    showMessage('错误', '创建失败', 'danger')
  } finally {
    submitting.value = false
  }
}

// 编辑轮播图
const editSwiper = (index) => {
  editingIndex.value = index
  const swiper = swiperList.value[index]
  form.value = {
    title: swiper.title || '',
    image: swiper.image
  }
  showEditModal.value = true
}

// 更新轮播图
const updateSwiper = async () => {
  if (!form.value.image) {
    showMessage('提示', '请选择图片', 'warning')
    return
  }
  
  submitting.value = true
  try {
    swiperList.value[editingIndex.value] = {
      title: form.value.title || '',
      image: form.value.image
    }
    
    closeModal()
  } catch (error) {
    console.error('更新轮播图失败:', error)
    showMessage('错误', '更新失败', 'danger')
  } finally {
    submitting.value = false
  }
}

// 删除轮播图
const deleteSwiper = (index) => {
  deletingIndex.value = index
  showDeleteConfirm.value = true
}

// 确认删除的处理函数
const confirmDelete = () => {
  try {
    swiperList.value.splice(deletingIndex.value, 1)
    showDeleteConfirm.value = false
  } catch (error) {
    console.error('删除轮播图失败:', error)
    showMessage('错误', '删除失败', 'danger')
  }
}

// 取消删除的处理函数
const cancelDelete = () => {
  showDeleteConfirm.value = false
  deletingIndex.value = -1
}

// 关闭模态框
const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingIndex.value = -1
  form.value = {
    title: '',
    image: ''
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

// 获取预览URL（添加token参数）
const getPreviewUrl = (imageUrl) => {
  return getImageUrlWithToken(imageUrl)
}

// 移动轮播图
const moveSwiper = (index, direction) => {
  const newIndex = direction === 'up' ? index - 1 : index + 1
  if (newIndex >= 0 && newIndex < swiperList.value.length) {
    const temp = swiperList.value[index]
    swiperList.value[index] = swiperList.value[newIndex]
    swiperList.value[newIndex] = temp
  }
}

// 组件挂载时获取数据
onMounted(() => {
  getSwiperConfig()
})
</script> 