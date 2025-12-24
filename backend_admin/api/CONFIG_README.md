# 配置系统说明

## 概述

本项目使用 `pydantic-settings` 来管理配置，支持从环境变量和 `.env` 文件读取配置。

## 配置项

### 应用配置
- `APP_NAME`: 应用名称 (默认: "后台管理系统")
- `DEBUG`: 调试模式 (默认: true)

### 安全配置
- `SECRET_KEY`: JWT 密钥 (默认: "your-secret-key-here-change-in-production")
- `ALGORITHM`: JWT 算法 (默认: "HS256")
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token 过期时间，单位分钟 (默认: 30)

### AccessKey 配置
- `ADMIN_ACCESS_KEY`: 管理员访问密钥 (默认: "admin123456")
- `ADMIN_USERNAME`: 管理员用户名 (默认: "admin")
- `ADMIN_PASSWORD`: 管理员密码 (默认: "admin123")

### CORS 配置
- `ALLOWED_ORIGINS`: 允许的域名列表 (默认: "*")

## 环境变量格式

### 基本格式
```bash
# 应用配置
APP_NAME=后台管理系统
DEBUG=true

# 安全配置
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AccessKey配置
ADMIN_ACCESS_KEY=admin123456
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# CORS配置
ALLOWED_ORIGINS=*
```

### CORS 配置说明

`ALLOWED_ORIGINS` 支持以下格式：

1. **允许所有域名** (开发环境推荐):
   ```bash
   ALLOWED_ORIGINS=*
   ```

2. **指定域名列表** (生产环境推荐):
   ```bash
   ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```

3. **多个域名**:
   ```bash
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,https://yourdomain.com
   ```

## 使用方法

### 1. 复制环境变量模板
```bash
cp env.example .env
```

### 2. 修改配置
编辑 `.env` 文件，根据需要修改配置项。

### 3. 在代码中使用

```python
from configs.config import settings

# 使用配置
app_name = settings.app_name
debug_mode = settings.debug
allowed_origins = settings.allowed_origins
```

## 配置优先级

1. 环境变量 (最高优先级)
2. `.env` 文件
3. 默认值 (最低优先级)

## 测试配置

运行测试脚本验证配置是否正确：
```bash
python test_config.py
```

## 注意事项

1. **生产环境安全**: 请务必修改 `SECRET_KEY`、`ADMIN_PASSWORD` 等敏感信息
2. **CORS 安全**: 生产环境不要使用 `ALLOWED_ORIGINS=*`，应该指定具体的域名
3. **环境变量**: 环境变量名称必须与配置项别名完全匹配
4. **类型转换**: 系统会自动处理类型转换，如字符串转布尔值、数字等 



部署方案

# 进入api目录
cd api

# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务