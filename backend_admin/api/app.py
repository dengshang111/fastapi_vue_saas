import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # 新增：用于挂载静态目录
from tortoise.contrib.fastapi import register_tortoise

from configs.config import ALLOWED_ORIGINS
from routers import (
    swiper, upload, phone, content,
    product, about, qr_code
)
from auth import login
from configs.database import TORTOISE_ORM


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用实例"""

    # 1. 初始化实例
    # 注意：如果使用了 register_tortoise，通常不需要在 FastAPI 构造函数中传 lifespan
    # 除非你的 lifespan 里还有其他非数据库的初始化逻辑
    app = FastAPI(
        title="后台管理系统API",
        description="SaaS 多端后台接口文档",
        version="1.0.0",
        debug=os.getenv("DEBUG", "False").lower() == "true"
    )

    # 2. 挂载上传文件夹 (让前端能访问 http://IP/uploads/...)
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

    # 3. 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 4. 注册路由 (建议添加前缀和标签)
    # 这样在 Swagger 文档中会按功能模块分组
    api_router_map = [
        (login.router, "认证模块", "/api"),
        (upload.router, "上传模块", "/api"),
        (swiper.router, "轮播图管理", "/api"),
        (product.router, "产品管理", "/api"),
        (content.router, "内容管理", "/api"),
        (phone.router, "联系方式", "/api"),
        (about.router, "关于我们", "/api"),
        (qr_code.router, "二维码工具", "/api"),
    ]

    for router, tag, prefix in api_router_map:
        app.include_router(router, prefix=prefix, tags=[tag])

    # 5. 配置 Tortoise ORM
    # register_tortoise 会自动处理连接和关闭
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=os.getenv("ENV") == "dev",  # 仅在开发环境自动建表
        add_exception_handlers=True,
    )

    return app