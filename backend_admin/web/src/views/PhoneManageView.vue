<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">电话号码管理</h1>
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
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">电话号码配置</h2>
          <div class="flex space-x-3">
            <button
              @click="showEditModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
              </svg>
              修改电话号码
            </button>
          </div>
        </div>

        <!-- 电话号码显示 -->
        <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">当前电话号码</h3>
                <p class="mt-1 max-w-2xl text-sm text-gray-500 dark:text-gray-400">用于显示在小程序中的联系电话</p>
              </div>
              <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ phoneNumber || '暂未设置' }}</div>
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
            加载中...
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-transparent overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">修改电话号码</h3>
          
          <form @submit.prevent="updatePhoneNumber" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">电话号码</label>
              <input
                v-model="form.phoneNumber"
                type="tel"
                class="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
                placeholder="请输入电话号码"
                pattern="[0-9]{11}"
                title="请输入11位手机号码"
                required
              />
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
                :disabled="submitting"
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const phoneNumber = ref('')
const loading = ref(false)
const submitting = ref(false)
const showEditModal = ref(false)

// 消息提示对话框相关的响应式数据
const showMessageDialog = ref(false)
const messageDialogConfig = ref({
  title: '',
  message: '',
  type: 'info'
})

// 表单数据
const form = ref({
  phoneNumber: ''
})

// 获取电话号码配置
const getPhoneConfig = async () => {
  loading.value = true
  try {
    const response = await authStore.authenticatedFetch('/api/phone/config')
    if (response.ok) {
      const data = await response.json()
      phoneNumber.value = data.phoneNumber || ''
    }
  } catch (error) {
    console.error('获取电话号码配置失败:', error)
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

// 更新电话号码
const updatePhoneNumber = async () => {
  if (!form.value.phoneNumber) {
    showMessage('提示', '请输入电话号码', 'warning')
    return
  }

  submitting.value = true
  try {
    const response = await authStore.authenticatedFetch('/api/phone/config', {
      method: 'PUT',
      body: JSON.stringify({
        phoneNumber: form.value.phoneNumber
      })
    })
    
    if (response.ok) {
      phoneNumber.value = form.value.phoneNumber
      showMessage('成功', '电话号码更新成功', 'info')
      closeModal()
    } else {
      const error = await response.json()
      showMessage('错误', error.detail || '更新失败', 'danger')
    }
  } catch (error) {
    console.error('更新电话号码失败:', error)
    showMessage('错误', '更新失败', 'danger')
  } finally {
    submitting.value = false
  }
}

// 关闭模态框
const closeModal = () => {
  showEditModal.value = false
  form.value = {
    phoneNumber: ''
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
  getPhoneConfig()
})
</script> 