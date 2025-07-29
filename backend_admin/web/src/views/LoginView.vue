<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
        后台管理系统
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
        请选择登录方式
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white dark:bg-gray-800 py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <!-- 登录方式切换 -->
        <div class="flex mb-6">
          <button
            @click="loginMethod = 'password'"
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-colors',
              loginMethod === 'password'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            ]"
          >
            用户名密码
          </button>
          <button
            @click="loginMethod = 'accessKey'"
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-colors',
              loginMethod === 'accessKey'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
            ]"
          >
            AccessKey
          </button>
        </div>

        <!-- 用户名密码登录 -->
        <form v-if="loginMethod === 'password'" @submit.prevent="handlePasswordLogin" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              用户名
            </label>
            <div class="mt-1">
              <input
                id="username"
                v-model="passwordForm.username"
                name="username"
                type="text"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="请输入用户名"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              密码
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="passwordForm.password"
                name="password"
                type="password"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="请输入密码"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading" class="inline-flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                登录中...
              </span>
              <span v-else>登录</span>
            </button>
          </div>
        </form>

        <!-- AccessKey登录 -->
        <form v-else @submit.prevent="handleAccessKeyLogin" class="space-y-6">
          <div>
            <label for="accessKey" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              AccessKey
            </label>
            <div class="mt-1">
              <input
                id="accessKey"
                v-model="accessKeyForm.accessKey"
                name="accessKey"
                type="password"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                placeholder="请输入AccessKey"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading" class="inline-flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                登录中...
              </span>
              <span v-else>使用AccessKey登录</span>
            </button>
          </div>
        </form>

        <!-- 错误信息 -->
        <div v-if="error" class="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
          <p class="text-sm text-red-600 dark:text-red-400">{{ error }}</p>
        </div>

        <!-- 提示信息 -->
        <div class="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
          <p v-if="loginMethod === 'password'">
            默认用户名: admin, 密码: admin123
          </p>
          <p v-else>
            AccessKey:29855e4c-ae10-4582-a473-ad544fce8b19
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const loginMethod = ref('password')
const loading = ref(false)
const error = ref('')

// 表单数据
const passwordForm = reactive({
  username: '',
  password: ''
})

const accessKeyForm = reactive({
  accessKey: ''
})

// 用户名密码登录
const handlePasswordLogin = async () => {
  if (!passwordForm.username || !passwordForm.password) {
    error.value = '请填写完整的登录信息'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await authStore.login(passwordForm.username, passwordForm.password)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// AccessKey登录
const handleAccessKeyLogin = async () => {
  if (!accessKeyForm.accessKey) {
    error.value = '请输入AccessKey'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await authStore.loginWithAccessKey(accessKeyForm.accessKey)
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script> 