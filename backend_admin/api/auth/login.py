from fastapi import APIRouter, Depends, HTTPException, status

from auth.auth import (
    create_access_token,
    verify_access_key,
    verify_admin_credentials,
    get_current_user
)
from models import LoginRequest, AccessKeyLoginRequest, TokenResponse, UserInfo, LogoutResponse
from configs.config import settings

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
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


@router.post("/login/access-key", response_model=TokenResponse)
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


@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: UserInfo = Depends(get_current_user)):
    """退出登录"""
    return LogoutResponse(message="退出登录成功")


@router.get("/user/info", response_model=UserInfo)
async def get_user_info(current_user: UserInfo = Depends(get_current_user)):
    """获取用户信息"""
    return current_user


@router.get("/dashboard")
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
