import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const accessKey = ref(localStorage.getItem('accessKey') || '')
  const isAuthenticated = computed(() => !!token.value)

  // API基础URL
  const API_BASE_URL = '/backend'

  // 设置认证信息
  const setAuth = (newToken, newUser, newAccessKey = '') => {
    token.value = newToken
    user.value = newUser
    accessKey.value = newAccessKey
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
    if (newAccessKey) {
      localStorage.setItem('accessKey', newAccessKey)
    }
  }

  // 清除认证信息
  const clearAuth = () => {
    token.value = ''
    user.value = null
    accessKey.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('accessKey')
  }

  // 用户名密码登录
  const login = async (username, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '登录失败')
      }

      const data = await response.json()
      setAuth(data.access_token, { username: data.username }, '')
      return data
    } catch (error) {
      throw error
    }
  }

  // AccessKey登录
  const loginWithAccessKey = async (accessKey) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/login/access-key`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ access_key: accessKey }),
      })
      console.log(response)
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'AccessKey登录失败')
      }

      const data = await response.json()
      setAuth(data.access_token, { username: data.username }, accessKey)
      return data
    } catch (error) {
      throw error
    }
  }

  // 退出登录
  const logout = async () => {
    try {
      if (token.value) {
        await fetch(`${API_BASE_URL}/api/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token.value}`,
            'Content-Type': 'application/json',
          },
        })
      }
    } catch (error) {
      console.error('退出登录时出错:', error)
    } finally {
      clearAuth()
    }
  }

  // 获取用户信息
  const getUserInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/info`, {
        headers: {
          'Authorization': `Bearer ${token.value}`,
        },
      })

      if (!response.ok) {
        throw new Error('获取用户信息失败')
      }

      const data = await response.json()
      user.value = data
      localStorage.setItem('user', JSON.stringify(data))
      return data
    } catch (error) {
      throw error
    }
  }

  // 带认证的fetch请求
  const authenticatedFetch = async (url, options = {}) => {
    const headers = {
      ...options.headers,
    }

    // 如果不是FormData，则设置Content-Type为JSON
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json'
    }

    if (token.value) {
      headers.Authorization = `Bearer ${token.value}`
    }

    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      clearAuth()
      router.push('/login')
      throw new Error('认证已过期，请重新登录')
    }

    return response
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    loginWithAccessKey,
    logout,
    getUserInfo,
    authenticatedFetch,
    clearAuth,
  }
}) 