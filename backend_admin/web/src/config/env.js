// 环境变量配置
export const config = {
  // 从环境变量获取SECRET_KEY，如果没有则使用默认值
  SECRET_KEY: import.meta.env.APP_SECRET_KEY || 'your_access_key',
  API_BASE_URL: '/backend', // 使用代理路径
  // 添加其他环境变量
  APP_NAME: import.meta.env.APP_APP_NAME || '后台管理系统',
  DEBUG: import.meta.env.APP_DEBUG === 'true',
  ALGORITHM: import.meta.env.APP_ALGORITHM || 'HS256',
  ACCESS_TOKEN_EXPIRE_MINUTES: parseInt(import.meta.env.APP_ACCESS_TOKEN_EXPIRE_MINUTES || '300'),
  ADMIN_ACCESS_KEY: import.meta.env.APP_ADMIN_ACCESS_KEY || 'admin123456',
  ADMIN_USERNAME: import.meta.env.APP_ADMIN_USERNAME || 'admin',
  ADMIN_PASSWORD: import.meta.env.APP_ADMIN_PASSWORD || 'admin123'
}

// 打印配置信息
const printConfig = () => {
  console.group('=== 当前环境配置信息 ===')
  Object.entries(config).forEach(([key, value]) => {
    // 对于敏感信息（如密钥），只显示前6位，其余用*代替
    const displayValue = key.includes('KEY') || key.includes('PASSWORD') ? 
      `${String(value).slice(0, 6)}${'*'.repeat(6)}` : 
      value
    console.log(`${key}: ${displayValue}`)
  })
  console.groupEnd()
}

// 在开发环境下打印配置信息
if (import.meta.env.DEV) {
  printConfig()
}

// 获取带token的图片URL
export const getImageUrlWithToken = (imageUrl) => {
  if (!imageUrl) return imageUrl
  
  // 如果已经是新的API路径格式，只添加token
  if (imageUrl.startsWith('/api/upload/static/')) {
    const separator = imageUrl.includes('?') ? '&' : '?'
    return `${config.API_BASE_URL}${imageUrl}${separator}token=${encodeURIComponent(config.SECRET_KEY)}&thumbnail=300x300`
  }
  
  return imageUrl
} 