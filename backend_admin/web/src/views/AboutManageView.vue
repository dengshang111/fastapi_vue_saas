<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">关于我们管理</h1>
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
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">关于我们配置</h2>
          <div class="flex space-x-3">
            <button
              @click="showCreateModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              添加内容块
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

        <!-- 内容块列表 -->
        <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-md">
          <div v-if="contentList.length === 0" class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">暂无内容</h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">开始添加您的第一个内容块吧。</p>
          </div>
          
          <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="(content, index) in contentList" :key="index" class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <!-- 内容类型图标 -->
                  <div class="flex-shrink-0">
                    <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="getTypeColor(content.type)">
                      <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                    </div>
                  </div>
                  
                  <!-- 内容信息 -->
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {{ content.title || '无标题' }}
                    </p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                      {{ content.subtitle || '无副标题' }}
                    </p>
                    <div class="flex items-center space-x-4 mt-1">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="getTypeBadgeColor(content.type)">
                        {{ getTypeLabel(content.type) }}
                      </span>
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
                    @click="moveContent(index, 'up')"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                    </svg>
                  </button>
                  <button
                    v-if="index < contentList.length - 1"
                    @click="moveContent(index, 'down')"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </button>
                  <button
                    @click="editContent(index)"
                    class="inline-flex items-center px-3 py-1 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                  >
                    编辑
                  </button>
                  <button
                    @click="deleteContent(index)"
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
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600 dark:text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-gray-900 dark:text-white">加载中...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑模态框 -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-transparent overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-200 shadow-lg rounded-md bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
            {{ showEditModal ? '编辑内容块' : '添加内容块' }}
          </h3>
          
          <form @submit.prevent="showEditModal ? updateContent() : createContent()" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">内容类型</label>
              <select
                v-model="form.type"
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                required
              >
                <option value="">请选择内容类型</option>
                <option value="title-card">标题卡片</option>
                <option value="section_header">章节标题</option>
                <option value="origin">起源/发展</option>
                <option value="mission">使命愿景</option>
                <option value="timeline">时间线</option>
                <option value="final-card">结束卡片</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">标题</label>
              <input
                v-model="form.title"
                type="text"
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="请输入标题"
                required
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">副标题</label>
              <input
                v-model="form.subtitle"
                type="text"
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="请输入副标题"
              />
            </div>
            
            <!-- 动态内容项 -->
            <div v-if="showItemsSection">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">内容项</label>
              <div class="space-y-2">
                <div v-for="(item, index) in form.items" :key="index" class="flex space-x-2">
                  <input
                    v-model="item.title"
                    type="text"
                    class="flex-1 border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="标题"
                  />
                  <input
                    v-model="item.text"
                    type="text"
                    class="flex-1 border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="内容"
                  />
                  <button
                    type="button"
                    @click="removeItem(index)"
                    class="px-3 py-2 border border-red-300 dark:border-red-600 text-red-700 dark:text-red-400 rounded-md hover:bg-red-50 dark:hover:bg-red-900"
                  >
                    删除
                  </button>
                </div>
                <button
                  type="button"
                  @click="addItem"
                  class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 bg-white dark:bg-gray-800"
                >
                  添加内容项
                </button>
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
                :disabled="submitting || !form.type || !form.title"
                class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
              >
                {{ submitting ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 消息提示对话框 -->
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

    <!-- 确认删除对话框 -->
    <ConfirmDialog
      v-model:show="showDeleteConfirm"
      title="删除确认"
      message="确定要删除这个内容块吗？"
      type="danger"
      confirmText="删除"
      cancelText="取消"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const contentList = ref([])
const loading = ref(false)
const saving = ref(false)
const submitting = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingIndex = ref(-1)

// 删除确认相关的响应式数据
const showDeleteConfirm = ref(false)
const deletingIndex = ref(-1)

// 消息提示对话框相关的响应式数据
const showMessageDialog = ref(false)
const messageDialogConfig = ref({
  title: '',
  message: '',
  type: 'info'
})

// 表单数据
const form = ref({
  type: '',
  title: '',
  subtitle: '',
  items: []
})

// 计算属性：是否显示内容项部分
const showItemsSection = computed(() => {
  return ['origin', 'mission', 'timeline'].includes(form.value.type)
})

// 获取内容类型标签
const getTypeLabel = (type) => {
  const labels = {
    'title-card': '标题卡片',
    'section_header': '章节标题',
    'origin': '起源/发展',
    'mission': '使命愿景',
    'timeline': '时间线',
    'final-card': '结束卡片'
  }
  return labels[type] || type
}

// 获取类型颜色
const getTypeColor = (type) => {
  const colors = {
    'title-card': 'bg-blue-500',
    'section_header': 'bg-green-500',
    'origin': 'bg-yellow-500',
    'mission': 'bg-purple-500',
    'timeline': 'bg-indigo-500',
    'final-card': 'bg-red-500'
  }
  return colors[type] || 'bg-gray-500'
}

// 获取类型徽章颜色
const getTypeBadgeColor = (type) => {
  const colors = {
    'title-card': 'bg-blue-100 text-blue-800',
    'section_header': 'bg-green-100 text-green-800',
    'origin': 'bg-yellow-100 text-yellow-800',
    'mission': 'bg-purple-100 text-purple-800',
    'timeline': 'bg-indigo-100 text-indigo-800',
    'final-card': 'bg-red-100 text-red-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

// 获取关于我们配置
const getAboutConfig = async () => {
  loading.value = true
  try {
    const response = await authStore.authenticatedFetch('/api/about/config')
    if (response.ok) {
      const data = await response.json()
      contentList.value = data.content || []
    }
  } catch (error) {
    console.error('获取关于我们配置失败:', error)
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

// 保存关于我们配置
const saveConfig = async () => {
  saving.value = true
  try {
    const response = await authStore.authenticatedFetch('/api/about/config', {
      method: 'PUT',
      body: JSON.stringify({
        content: contentList.value
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

// 创建内容块
const createContent = async () => {
  if (!form.value.type || !form.value.title) {
    showMessage('提示', '请填写必填字段', 'warning')
    return
  }
  
  submitting.value = true
  try {
    const newContent = {
      type: form.value.type,
      title: form.value.title,
      subtitle: form.value.subtitle || ''
    }
    
    // 如果有内容项，添加到新内容中
    if (showItemsSection.value && form.value.items.length > 0) {
      newContent.items = form.value.items
    }
    
    contentList.value.push(newContent)
    
    closeModal()
  } catch (error) {
    console.error('创建内容块失败:', error)
    showMessage('错误', '创建失败', 'danger')
  } finally {
    submitting.value = false
  }
}

// 编辑内容块
const editContent = (index) => {
  editingIndex.value = index
  const content = contentList.value[index]
  form.value = {
    type: content.type,
    title: content.title,
    subtitle: content.subtitle || '',
    items: content.items || []
  }
  showEditModal.value = true
}

// 更新内容块
const updateContent = async () => {
  if (!form.value.type || !form.value.title) {
    showMessage('提示', '请填写必填字段', 'warning')
    return
  }
  
  submitting.value = true
  try {
    const updatedContent = {
      type: form.value.type,
      title: form.value.title,
      subtitle: form.value.subtitle || ''
    }
    
    // 如果有内容项，添加到更新内容中
    if (showItemsSection.value && form.value.items.length > 0) {
      updatedContent.items = form.value.items
    }
    
    contentList.value[editingIndex.value] = updatedContent
    
    closeModal()
  } catch (error) {
    console.error('更新内容块失败:', error)
    showMessage('错误', '更新失败', 'danger')
  } finally {
    submitting.value = false
  }
}

// 删除内容块
const deleteContent = (index) => {
  deletingIndex.value = index
  showDeleteConfirm.value = true
}

// 确认删除的处理函数
const confirmDelete = () => {
  try {
    contentList.value.splice(deletingIndex.value, 1)
    showDeleteConfirm.value = false
  } catch (error) {
    console.error('删除内容块失败:', error)
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
    type: '',
    title: '',
    subtitle: '',
    items: []
  }
}

// 添加内容项
const addItem = () => {
  form.value.items.push({
    title: '',
    text: ''
  })
}

// 删除内容项
const removeItem = (index) => {
  form.value.items.splice(index, 1)
}

// 移动内容块
const moveContent = (index, direction) => {
  const newIndex = direction === 'up' ? index - 1 : index + 1
  if (newIndex >= 0 && newIndex < contentList.value.length) {
    const temp = contentList.value[index]
    contentList.value[index] = contentList.value[newIndex]
    contentList.value[newIndex] = temp
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

// 组件挂载时获取数据
onMounted(() => {
  getAboutConfig()
})
</script> 