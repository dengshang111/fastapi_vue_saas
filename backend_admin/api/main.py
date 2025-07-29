from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import timedelta
import uvicorn
import os

from config import settings, ALLOWED_ORIGINS
from auth import create_access_token, verify_token, verify_access_key, verify_admin_credentials, get_current_user
from models import LoginRequest, AccessKeyLoginRequest, TokenResponse, UserInfo, LogoutResponse
from routers import swiper, upload, phone, content, product, about, qr_code

app = FastAPI(title=settings.app_name, debug=settings.debug)

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

@app.get("/")
async def root():
    return {"message": "后台管理系统API", "version": "1.0.0"}

@app.post("/api/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """用户名密码登录"""
    if not verify_admin_credentials(login_data.username, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    access_token = create_access_token(
        data={"sub": login_data.username}
    )
    
    return TokenResponse(
        access_token=access_token,
        username=login_data.username
    )

@app.post("/api/login/access-key", response_model=TokenResponse)
async def login_with_access_key(login_data: AccessKeyLoginRequest):
    """AccessKey登录"""
    if not verify_access_key(login_data.access_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="AccessKey无效"
        )
    
    access_token = create_access_token(
        data={"sub": settings.admin_username}
    )
    
    return TokenResponse(
        access_token=access_token,
        username=settings.admin_username
    )

@app.post("/api/logout", response_model=LogoutResponse)
async def logout(current_user: UserInfo = Depends(get_current_user)):
    """退出登录"""
    return LogoutResponse(message="退出登录成功")

@app.get("/api/user/info", response_model=UserInfo)
async def get_user_info(current_user: UserInfo = Depends(get_current_user)):
    """获取用户信息"""
    return current_user

@app.get("/api/dashboard")
async def get_dashboard(current_user: UserInfo = Depends(get_current_user)):
    """获取仪表板数据"""
    return {
        "message": f"欢迎 {current_user.username}",
        "stats": {
            "total_users": 100,
            "active_users": 85,
            "total_orders": 1250,
            "revenue": 50000
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=13286, reload=True) 