<template>
  <div class="min-h-screen bg-gray-100  dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">用户管理</h1>
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
        <!-- 分组和操作栏 -->
        <div class="mb-6 space-y-4">
          <!-- 分组选择 -->
          <div class="flex items-center space-x-4">
            <label class="text-sm font-medium text-gray-700 dark:text-gray-300">分组:</label>
            <select
              v-model="currentGroup"
              @change="onGroupChange"
              class="border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-200 dark:focus:ring-blue-400"
            >
              <option value="">默认分组</option>
              <option v-for="group in groups" :key="group.name" :value="group.name">
                {{ group.name }} ({{ group.file_count }})
              </option>
            </select>
            <button
              @click="showCreateGroupModal = true"
              class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              新建分组
            </button>
            <button
              v-if="currentGroup"
              @click="deleteCurrentGroup"
              class="inline-flex items-center px-3 py-2 border border-red-300 dark:border-red-600 text-sm font-medium rounded-md text-red-700 dark:text-red-400 bg-white dark:bg-gray-700 hover:bg-red-50 dark:hover:bg-red-900/20"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              删除分组
            </button>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-between items-center">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">图片文件管理</h2>
            <div class="flex items-center space-x-2">
              <!-- 批量操作 -->
              <div v-if="selectedFiles.length > 0" class="flex items-center space-x-2">
                <span class="text-sm text-gray-600 dark:text-gray-400">已选择 {{ selectedFiles.length }} 个文件</span>
                <button
                  @click="batchDelete"
                  class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                  批量删除
                </button>
                <button
                  @click="clearSelection"
                  class="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                >
                  取消选择
                </button>
              </div>
              
              <!-- 上传按钮 -->
              <button
                @click="showUploadModal = true"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                上传图片
              </button>
            </div>
          </div>
        </div>

        <!-- 图片网格 -->
        <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
          <!-- 加载状态 -->
          <div v-if="loading" class="text-center py-8">
            <div class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600 dark:text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="text-gray-600 dark:text-gray-400">加载中...</span>
            </div>
          </div>

          <!-- 图片网格 -->
          <div v-else class="p-6">
            <!-- 全选功能 -->
            <div v-if="displayedFiles.length > 0" class="mb-4 flex items-center space-x-2">
              <input
                type="checkbox"
                :checked="isAllSelected"
                @change="toggleSelectAll"
                class="w-4 h-4 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:bg-gray-700"
              />
              <label class="text-sm font-medium text-gray-700 dark:text-gray-300">
                全选 ({{ displayedFiles.length }})
              </label>
              <span v-if="selectedFiles.length > 0" class="text-sm text-gray-500 dark:text-gray-400">
                - 已选择 {{ selectedFiles.length }} 个
              </span>
            </div>
            
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
              <div
                v-for="(file, index) in displayedFiles"
                :key="file.filename"
                class="relative group"
                :ref="el => { if (el) fileRefs[index] = el }"
                :data-index="index"
                @click="toggleFileSelection(file)"
              >
                <!-- 选择框 -->
                <div class="absolute top-2 left-2 z-10">
                  <input
                    type="checkbox"
                    :checked="selectedFiles.includes(file.filename)"
                    @click.stop
                    @change="toggleFileSelection(file)"
                    class="w-4 h-4 text-blue-600 border-gray-300 dark:border-gray-600 rounded focus:ring-blue-500 dark:bg-gray-700"
                  />
                </div>
                <!-- 图片容器 -->
                <div class="aspect-square bg-gray-100 dark:bg-gray-700 rounded-lg overflow-hidden">
                  <!-- 懒加载图片 - 低分辨率缩略图 -->
                  <img
                    v-if="file.isVisible"
                    :src="getThumbnailUrl(file.url)"
                    :alt="file.filename"
                    class="w-full h-full object-cover transition-opacity duration-300"
                    @load="onImageLoad(index)"
                    @error="onImageError(index)"
                    loading="lazy"
                  />
                  <!-- 占位符 -->
                  <div v-else class="w-full h-full flex items-center justify-center">
                    <svg class="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                </div>

                <!-- 文件名 -->
                <p class="mt-2 text-xs text-gray-600 dark:text-gray-400 truncate">{{ file.filename }}</p>
                
                <!-- 文件大小 -->
                <p class="text-xs text-gray-500 dark:text-gray-500">{{ formatFileSize(file.size) }}</p>

                <!-- 操作按钮 -->
                <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  <div class="flex space-x-1">
                    <!-- 预览按钮 -->
                    <button
                      @click="previewImage(file)"
                      class="p-1 bg-blue-500 text-white rounded-full hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 transition-colors"
                      title="预览"
                    >
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                      </svg>
                    </button>
                    
                    <!-- 删除按钮 -->
                    <button
                      @click="deleteFile(file)"
                      class="p-1 bg-red-500 text-white rounded-full hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700 transition-colors"
                      title="删除"
                    >
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-if="!loading && displayedFiles.length === 0" class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">暂无图片</h3>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">开始上传您的第一张图片吧。</p>
            </div>

            <!-- 加载更多 -->
            <div v-if="hasMore && !loading" class="text-center py-4">
              <button
                @click="loadMore"
                class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                加载更多
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 上传模态框 -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-transparent  h-full w-full z-50 ">
      <div class="relative top-20 mx-auto p-5 border w-200 shadow-lg rounded-md bg-white dark:bg-gray-800 dark:border-gray-700">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4 dark:text-gray-100">上传图片</h3>
          
          <!-- 分组选择 -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2 dark:text-gray-200">选择分组</label>
            <select
              v-model="uploadGroup"
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100"
            >
              <option value="">默认分组</option>
              <option v-for="group in groups" :key="group.name" :value="group.name">
                {{ group.name }}
              </option>
            </select>
          </div>
          
          <ImageUpload :group="uploadGroup" @upload-success="handleUploadSuccess" />
          
          <div class="flex justify-end space-x-3 pt-4">
            <button
              @click="showUploadModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600 dark:hover:bg-gray-600"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建分组模态框 -->
    <div v-if="showCreateGroupModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 dark:bg-gray-900 dark:bg-opacity-80">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800 dark:border-gray-700">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4 dark:text-gray-100">新建分组</h3>
          
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2 dark:text-gray-200">分组名称</label>
            <input
              v-model="newGroupName"
              type="text"
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100"
              placeholder="请输入分组名称"
            />
          </div>
          
          <div class="flex justify-end space-x-3 pt-4">
            <button
              @click="showCreateGroupModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600 dark:hover:bg-gray-600"
            >
              取消
            </button>
            <button
              @click="createGroup"
              :disabled="!newGroupName.trim()"
              class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 dark:bg-blue-700 dark:hover:bg-blue-800"
            >
              创建
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片预览模态框 -->
    <div v-if="showPreviewModal" class="fixed inset-0 bg-black bg-opacity-75 dark:bg-black dark:bg-opacity-90 overflow-y-auto h-full w-full z-50">
      <div class="relative top-10 mx-auto p-5 max-w-4xl">
        <div class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden">
          <div class="flex justify-between items-center p-4 border-b dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">{{ previewFile?.filename }}</h3>
            <button
              @click="showPreviewModal = false"
              class="text-gray-400 hover:text-gray-600 dark:text-gray-300 dark:hover:text-gray-100"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div class="p-4">
            <img
              :src="getImageUrlWithToken(previewFile?.url)"
              :alt="previewFile?.filename"
              class="w-full h-auto max-h-96 object-contain"
              loading="eager"
            />
            <div class="mt-4 text-sm text-gray-600 dark:text-gray-300">
              <p>文件名: {{ previewFile?.filename }}</p>
              <p>大小: {{ formatFileSize(previewFile?.size) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 确认对话框 -->
    <ConfirmDialog
      :show="showConfirmDialog"
      :title="confirmDialog.title"
      :message="confirmDialog.message"
      :type="confirmDialog.type"
      :confirm-text="confirmDialog.confirmText"
      :cancel-text="confirmDialog.cancelText"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />

    <!-- 提示消息 -->
    <Toast
      :show="showToast"
      :title="toast.title"
      :message="toast.message"
      :type="toast.type"
      :duration="toast.duration"
      @close="showToast = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ImageUpload from '../components/ImageUpload.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import Toast from '../components/Toast.vue'
import { getImageUrlWithToken } from '../config/env'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const files = ref([])
const loading = ref(false)
const showUploadModal = ref(false)
const showPreviewModal = ref(false)
const showCreateGroupModal = ref(false)
const previewFile = ref(null)
const fileRefs = ref([])

// 确认对话框相关
const showConfirmDialog = ref(false)
const confirmDialog = ref({
  title: '',
  message: '',
  type: 'info',
  confirmText: '确定',
  cancelText: '取消',
  onConfirm: null
})

// 提示消息相关
const showToast = ref(false)
const toast = ref({
  title: '',
  message: '',
  type: 'info',
  duration: 3000
})

// 分组相关
const groups = ref([])
const currentGroup = ref('')
const uploadGroup = ref('')
const newGroupName = ref('')

// 批量操作相关
const selectedFiles = ref([])

// 分页参数
const pageSize = 24 // 每页显示24张图片
const currentPage = ref(1)

// 懒加载相关
const observer = ref(null)
const visibleFiles = ref(new Set())

// 计算属性
const displayedFiles = computed(() => {
  const start = 0
  const end = currentPage.value * pageSize
  return files.value.slice(start, end).map(file => ({
    ...file,
    isVisible: visibleFiles.value.has(file.filename)
  }))
})

const hasMore = computed(() => {
  return currentPage.value * pageSize < files.value.length
})

// 全选状态计算属性
const isAllSelected = computed(() => {
  return displayedFiles.value.length > 0 && 
         displayedFiles.value.every(file => selectedFiles.value.includes(file.filename))
})

// 获取文件列表
const getFiles = async () => {
  loading.value = true
  try {
    const url = currentGroup.value 
      ? `/api/upload/files?group=${encodeURIComponent(currentGroup.value)}`
      : '/api/upload/files'
    const response = await authStore.authenticatedFetch(url)
    if (response.ok) {
      const data = await response.json()
      // 文件URL已经是完整的static路径，直接使用
      files.value = data
    }
  } catch (error) {
    console.error('获取文件列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取分组列表
const getGroups = async () => {
  try {
    const response = await authStore.authenticatedFetch('/api/upload/groups')
    if (response.ok) {
      groups.value = await response.json()
    }
  } catch (error) {
    console.error('获取分组列表失败:', error)
  }
}

// 加载更多
const loadMore = () => {
  currentPage.value++
}

// 处理上传成功
const handleUploadSuccess = (result) => {
  console.log('图片上传成功:', result)
  showUploadModal.value = false
  uploadGroup.value = ''
  // 重新获取文件列表和分组列表
  getFiles()
  getGroups()
}

// 分组变化处理
const onGroupChange = () => {
  currentPage.value = 1
  selectedFiles.value = []
  getFiles()
}

// 创建分组
const createGroup = async () => {
  if (!newGroupName.value.trim()) return
  
  try {
    const response = await authStore.authenticatedFetch('/api/upload/groups', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: newGroupName.value.trim() })
    })
    
    if (response.ok) {
      const createdGroupName = newGroupName.value.trim()
      showCreateGroupModal.value = false
      newGroupName.value = ''
      await getGroups()
      showMessage({
        title: '创建成功',
        message: `分组 "${createdGroupName}" 已创建`,
        type: 'success'
      })
    } else {
      const error = await response.json()
      showMessage({
        title: '创建失败',
        message: error.detail || '创建分组失败',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('创建分组失败:', error)
    showMessage({
      title: '创建失败',
      message: '创建分组失败',
      type: 'error'
    })
  }
}

// 显示确认对话框
const showConfirm = (options) => {
  confirmDialog.value = {
    title: options.title || '确认',
    message: options.message || '确定要执行此操作吗？',
    type: options.type || 'info',
    confirmText: options.confirmText || '确定',
    cancelText: options.cancelText || '取消',
    onConfirm: options.onConfirm
  }
  showConfirmDialog.value = true
}

// 显示提示消息
const showMessage = (options) => {
  toast.value = {
    title: options.title || '',
    message: options.message || '',
    type: options.type || 'info',
    duration: options.duration || 3000
  }
  showToast.value = true
}

// 处理确认对话框确认
const handleConfirm = () => {
  showConfirmDialog.value = false
  if (confirmDialog.value.onConfirm) {
    confirmDialog.value.onConfirm()
  }
}

// 处理确认对话框取消
const handleCancel = () => {
  showConfirmDialog.value = false
}

// 删除当前分组
const deleteCurrentGroup = async () => {
  if (!currentGroup.value) return
  
  showConfirm({
    title: '删除分组',
    message: `确定要删除分组 "${currentGroup.value}" 吗？\n注意：只有空分组才能被删除。`,
    type: 'danger',
    confirmText: '删除',
    cancelText: '取消',
    onConfirm: async () => {
      try {
        const response = await authStore.authenticatedFetch(`/api/upload/groups/${encodeURIComponent(currentGroup.value)}`, {
          method: 'DELETE'
        })
        
        if (response.ok) {
          // 删除成功，切换到默认分组
          const deletedGroupName = currentGroup.value
          currentGroup.value = ''
          selectedFiles.value = []
          await getGroups()
          await getFiles()
          showMessage({
            title: '删除成功',
            message: `分组 "${deletedGroupName}" 已删除`,
            type: 'success'
          })
        } else {
          const error = await response.json()
          showMessage({
            title: '删除失败',
            message: error.detail || '删除分组失败',
            type: 'error'
          })
        }
      } catch (error) {
        console.error('删除分组失败:', error)
        showMessage({
          title: '删除失败',
          message: '删除分组失败',
          type: 'error'
        })
      }
    }
  })
}

// 切换文件选择
const toggleFileSelection = (file) => {
  const index = selectedFiles.value.indexOf(file.filename)
  if (index > -1) {
    selectedFiles.value.splice(index, 1)
  } else {
    selectedFiles.value.push(file.filename)
  }
}

// 全选/取消全选
const toggleSelectAll = () => {
  if (isAllSelected.value) {
    // 取消全选 - 移除所有当前显示的文件
    displayedFiles.value.forEach(file => {
      const index = selectedFiles.value.indexOf(file.filename)
      if (index > -1) {
        selectedFiles.value.splice(index, 1)
      }
    })
  } else {
    // 全选 - 添加所有当前显示的文件
    displayedFiles.value.forEach(file => {
      if (!selectedFiles.value.includes(file.filename)) {
        selectedFiles.value.push(file.filename)
      }
    })
  }
}

// 批量删除
const batchDelete = async () => {
  if (selectedFiles.value.length === 0) return
  
  showConfirm({
    title: '批量删除',
    message: `确定要删除选中的 ${selectedFiles.value.length} 个文件吗？`,
    type: 'danger',
    confirmText: '删除',
    cancelText: '取消',
    onConfirm: async () => {
      try {
        const response = await authStore.authenticatedFetch('/api/upload/batch-delete', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ filenames: selectedFiles.value })
        })
        
        if (response.ok) {
          // 从列表中移除已删除的文件
          const deletedCount = selectedFiles.value.length
          files.value = files.value.filter(file => !selectedFiles.value.includes(file.filename))
          selectedFiles.value = []
          // 更新分组列表
          getGroups()
          showMessage({
            title: '删除成功',
            message: `成功删除 ${deletedCount} 个文件`,
            type: 'success'
          })
        } else {
          const error = await response.json()
          showMessage({
            title: '删除失败',
            message: error.detail || '批量删除失败',
            type: 'error'
          })
        }
      } catch (error) {
        console.error('批量删除失败:', error)
        showMessage({
          title: '删除失败',
          message: '批量删除失败',
          type: 'error'
        })
      }
    }
  })
}

// 清除选择
const clearSelection = () => {
  selectedFiles.value = []
}

// 删除文件
const deleteFile = async (file) => {
  showConfirm({
    title: '删除文件',
    message: `确定要删除文件 "${file.filename}" 吗？`,
    type: 'danger',
    confirmText: '删除',
    cancelText: '取消',
    onConfirm: async () => {
      try {
        // 根据文件是否在分组中决定删除路径
        let deleteUrl
        if (file.group && currentGroup.value) {
          // 文件在分组中，使用分组删除路径
          deleteUrl = `/api/upload/image/${encodeURIComponent(currentGroup.value)}/${file.filename}`
        } else {
          // 文件在默认分组中，使用默认删除路径
          deleteUrl = `/api/upload/image/${file.filename}`
        }
        
        const response = await authStore.authenticatedFetch(deleteUrl, {
          method: 'DELETE'
        })
        console.log(deleteUrl)
        if (response.ok) {
          // 从列表中移除
          const index = files.value.findIndex(f => f.filename === file.filename)
          if (index > -1) {
            files.value.splice(index, 1)
          }
          // 从选中列表中移除该文件
          const selectedIndex = selectedFiles.value.indexOf(file.filename)
          if (selectedIndex > -1) {
            selectedFiles.value.splice(selectedIndex, 1)
          }
          // 更新分组列表
          getGroups()
          showMessage({
            title: '删除成功',
            message: `文件 "${file.filename}" 已删除`,
            type: 'success'
          })
        } else {
          const error = await response.json()
          showMessage({
            title: '删除失败',
            message: error.detail || '删除失败',
            type: 'error'
          })
        }
      } catch (error) {
        console.error('删除文件失败:', error)
        showMessage({
          title: '删除失败',
          message: '删除失败',
          type: 'error'
        })
      }
    }
  })
}

// 预览图片
const previewImage = (file) => {
  previewFile.value = file
  showPreviewModal.value = true
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 获取缩略图URL
const getThumbnailUrl = (url) => {
  if (!url) return ''
  // 先添加token参数
  const urlWithToken = getImageUrlWithToken(url)
  // 再添加缩略图参数，限制图片尺寸为300x300
  const separator = urlWithToken.includes('?') ? '&' : '?'
  return `${urlWithToken}${separator}thumbnail=300x300`
}

// 图片加载完成
const onImageLoad = (index) => {
  // 图片加载成功，可以添加一些处理逻辑
}

// 图片加载失败
const onImageError = (index) => {
  // 图片加载失败，可以显示默认图片
}

// 设置懒加载观察器
const setupIntersectionObserver = () => {
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const index = parseInt(entry.target.dataset.index)
        const file = displayedFiles.value[index]
        if (file) {
          visibleFiles.value.add(file.filename)
        }
      }
    })
  }, {
    rootMargin: '50px' // 提前50px开始加载
  })
}

 // 观察元素
 const observeElements = () => {
   nextTick(() => {
     fileRefs.value.forEach((el, index) => {
       if (el && observer.value) {
         observer.value.observe(el)
       }
     })
   })
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

// 组件挂载
onMounted(() => {
  getGroups()
  getFiles()
  setupIntersectionObserver()
})

// 组件卸载
onUnmounted(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
})

// 监听文件列表变化，重新观察元素
watch(displayedFiles, () => {
  observeElements()
}, { deep: true })
</script> 