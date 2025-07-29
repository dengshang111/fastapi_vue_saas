<template>
  <view class="api-demo">
    <view class="header">
      <text class="title">API 演示页面</text>
    </view>
    
    <view class="section">
      <text class="section-title">登录状态</text>
      <view class="status-card">
        <text class="status-text">Token: {{ tokenStatus }}</text>
        <text class="username-text">用户名: {{ username }}</text>
      </view>
    </view>
    
    <view class="section">
      <text class="section-title">操作按钮</text>
      <view class="button-group">
        <button class="btn btn-primary" @click="handleLogin">获取新Token</button>
        <button class="btn btn-secondary" @click="handleLogout">清除Token</button>
        <button class="btn btn-success" @click="handleTestRequest">测试请求</button>
      </view>
    </view>
    
    <view class="section">
      <text class="section-title">请求结果</text>
      <view class="result-card">
        <text class="result-text">{{ requestResult }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { login, getToken, clearToken, request } from '../../utils/api.js'

const tokenStatus = ref('未获取')
const username = ref('未获取')
const requestResult = ref('暂无结果')

// 检查登录状态
const checkLoginStatus = () => {
  const token = getToken()
  const storedUsername = uni.getStorageSync('username')
  
  if (token) {
    tokenStatus.value = '已登录'
    username.value = storedUsername || '未知'
  } else {
    tokenStatus.value = '未登录'
    username.value = '未获取'
  }
}

// 手动登录（获取新token）
const handleLogin = async () => {
  try {
    uni.showLoading({ title: '登录中...' })
    const accessKey = '29855e4c-ae10-4582-a473-ad544fce8b19'
    const result = await login(accessKey)
    
    uni.hideLoading()
    uni.showToast({
      title: '登录成功',
      icon: 'success'
    })
    
    checkLoginStatus()
    requestResult.value = JSON.stringify(result, null, 2)
  } catch (error) {
    uni.hideLoading()
    uni.showToast({
      title: '登录失败',
      icon: 'error'
    })
    requestResult.value = `登录失败: ${error.message}`
  }
}

// 清除Token
const handleLogout = () => {
  clearToken()
  uni.removeStorageSync('username')
  checkLoginStatus()
  requestResult.value = 'Token已清除'
  
  uni.showToast({
    title: '已退出登录',
    icon: 'success'
  })
}

// 测试请求（带token）
const handleTestRequest = async () => {
  try {
    uni.showLoading({ title: '请求中...' })
    
    // 这里可以替换为你的实际API接口
    const result = await request({
      url: 'https://api.jeremy233.club/api/test', // 替换为你的测试接口
      method: 'GET'
    })
    
    uni.hideLoading()
    requestResult.value = JSON.stringify(result, null, 2)
  } catch (error) {
    uni.hideLoading()
    requestResult.value = `请求失败: ${error.message}`
    
    uni.showToast({
      title: '请求失败',
      icon: 'error'
    })
  }
}

onMounted(() => {
  checkLoginStatus()
})
</script>

<style lang="scss" scoped>
.api-demo {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  
  .title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
  }
}

.section {
  margin-bottom: 30px;
  
  .section-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 15px;
    display: block;
  }
}

.status-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  
  .status-text {
    display: block;
    margin-bottom: 10px;
    color: #666;
  }
  
  .username-text {
    display: block;
    color: #666;
  }
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.btn {
  padding: 15px 20px;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  font-weight: bold;
  
  &.btn-primary {
    background-color: #007aff;
    color: white;
  }
  
  &.btn-secondary {
    background-color: #ff3b30;
    color: white;
  }
  
  &.btn-success {
    background-color: #34c759;
    color: white;
  }
}

.result-card {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-height: 100px;
  
  .result-text {
    font-family: monospace;
    font-size: 12px;
    color: #333;
    word-break: break-all;
    white-space: pre-wrap;
  }
}
</style> 