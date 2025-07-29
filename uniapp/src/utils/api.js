// API服务文件
const BASE_URL = 'https://api.jeremy233.club/api'

// 获取存储的token
const getToken = () => {
  return uni.getStorageSync('access_token') || ''
}

// 设置token
const setToken = (token) => {
  uni.setStorageSync('access_token', token)
}

// 清除token
const clearToken = () => {
  uni.removeStorageSync('access_token')
}

// 登录接口
export const login = (accessKey) => {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}/login/access-key`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'accept': 'application/json'
      },
      data: {
        access_key: accessKey
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const { access_token, username } = res.data
          setToken(access_token)
          uni.setStorageSync('username', username)
          resolve(res.data)
        } else {
          reject(new Error('登录失败'))
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

// 通用请求方法（带token）
export const request = (options) => {
  return new Promise((resolve, reject) => {
    const token = getToken()
    
    const requestOptions = {
      ...options,
      header: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        ...options.header
      }
    }
    
    // 如果有token，添加到请求头
    if (token) {
      requestOptions.header.Authorization = `Bearer ${token}`
    }
    
    uni.request({
      ...requestOptions,
      success: (res) => {
        // 如果返回401，说明token过期，清除token
        if (res.statusCode === 401) {
          clearToken()
          // 可以在这里重新登录或跳转到登录页
          uni.showToast({
            title: '登录已过期，请重新登录',
            icon: 'none'
          })
        }
        resolve(res)
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

// 导出token管理方法
export { getToken, setToken, clearToken } 