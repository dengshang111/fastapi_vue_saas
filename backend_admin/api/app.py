from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOWED_ORIGINS
from routers import (
    swiper, upload, phone, content,
    product, about, qr_code
)
from auth import login


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    app = FastAPI(title="后台管理系统API", debug=True)

    # 配置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(swiper.router)
    app.include_router(upload.router)
    app.include_router(phone.router)
    app.include_router(content.router)
    app.include_router(product.router)
    app.include_router(about.router)
    app.include_router(qr_code.router)
    app.include_router(login.router)

    return app
