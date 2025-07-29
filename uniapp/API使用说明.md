# 微信小程序 API 使用说明

## 功能概述

本项目已集成自动登录功能，每次打开小程序时会自动执行登录操作，并将获取到的 `access_token` 存储到本地，所有后续的API请求都会自动携带这个token。

## 文件结构

```
src/
├── utils/
│   └── api.js          # API服务文件，包含登录和请求方法
├── pages/index/
│   └── api-demo.vue    # API演示页面
└── App.vue             # 应用入口，包含自动登录逻辑
```

## 核心功能

### 1. 自动登录
- 在 `App.vue` 的 `onLaunch` 生命周期中自动执行登录
- 使用固定的 `access_key` 进行登录
- 每次启动都会获取新的token，确保token不会过期
- 登录成功后将 `access_token` 和 `username` 存储到本地

### 2. Token 管理
- `getToken()`: 获取存储的token
- `setToken(token)`: 设置token
- `clearToken()`: 清除token

### 3. 请求拦截
- `request()` 方法会自动为所有请求添加 `Authorization: Bearer {token}` 头
- 如果请求返回401，会自动清除token并提示重新登录

## 使用方法

### 基本登录
```javascript
import { login } from './utils/api.js'

// 登录
const result = await login('29855e4c-ae10-4582-a473-ad544fce8b19')
console.log('登录成功:', result)
```

### 带Token的请求
```javascript
import { request } from './utils/api.js'

// 发送带token的请求
const result = await request({
  url: 'https://api.jeremy233.club/api/your-endpoint',
  method: 'POST',
  data: {
    // 你的请求数据
  }
})
```

### 检查登录状态
```javascript
import { getToken } from './utils/api.js'

const token = getToken()
if (token) {
  console.log('已登录')
} else {
  console.log('未登录')
}
```

## API 接口说明

### 登录接口
- **URL**: `https://api.jeremy233.club/api/login/access-key`
- **方法**: POST
- **请求体**:
  ```json
  {
    "access_key": "29855e4c-ae10-4582-a473-ad544fce8b19"
  }
  ```
- **响应**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "username": "admin"
  }
  ```

## 演示页面

访问 `/pages/index/api-demo` 页面可以：
1. 查看当前登录状态
2. 手动执行登录
3. 清除token
4. 测试带token的API请求

## 注意事项

1. **Token 存储**: token存储在本地存储中，小程序关闭后仍然保留
2. **自动登录**: 每次打开小程序都会自动登录获取新的token，确保token不会过期
3. **错误处理**: 如果登录失败或token过期，会显示相应的错误提示
4. **网络请求**: 所有使用 `request()` 方法的请求都会自动携带token

## 自定义配置

如果需要修改登录参数或API地址，可以编辑以下文件：

1. **修改 access_key**: 在 `App.vue` 和 `api-demo.vue` 中修改
2. **修改 API 地址**: 在 `utils/api.js` 中修改 `BASE_URL`
3. **修改请求头**: 在 `utils/api.js` 的 `request()` 方法中修改

## 测试

1. 打开小程序，查看控制台是否有"登录成功"的日志
2. 访问 API 演示页面，检查登录状态
3. 尝试发送测试请求，确认token正常工作 