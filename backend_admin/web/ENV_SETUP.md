# 环境变量配置说明

## 必需的环境变量

在 `web` 目录下创建 `.env` 文件，包含以下配置：

```env
# 静态文件访问的SECRET_KEY（必须与后端ACCESS_KEY一致）
VITE_SECRET_KEY=your_access_key
```

## 代理配置

项目已配置Vite代理，所有API请求都会通过 `/backend` 路径代理到后端服务器：

- 前端请求：`/backend/api/login`
- 实际请求：`http://localhost:8000/api/login`

这样可以解决前后端分离的跨域问题。

## 配置说明

1. **VITE_SECRET_KEY**: 用于访问静态文件的token，必须与后端 `ACCESS_KEY` 环境变量保持一致
2. **代理配置**: 所有API请求通过 `/backend` 路径代理到后端服务器

## 注意事项

- 所有以 `VITE_` 开头的环境变量都会被Vite打包到前端代码中
- 修改环境变量后需要重启开发服务器
- 代理配置只在开发环境生效，生产环境需要配置nginx等反向代理
- 确保后端服务器运行在 `http://localhost:8000`

## 后端配置

确保后端也设置了相应的环境变量：

```bash
export ACCESS_KEY=your_access_key
```

或者在启动后端时设置：

```bash
ACCESS_KEY=your_access_key python main.py
``` 