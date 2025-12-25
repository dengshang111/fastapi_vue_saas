from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.auth import (
    create_access_token,
    verify_access_key,
    verify_admin_credentials,
    get_current_user
)
from models import (
    LoginRequest, AccessKeyLoginRequest, TokenResponse,
    UserInfo, LogoutResponse
)
from configs.config import settings

# 建议不要在这里写死 /api，而是在 create_app 注册时统一指定
router = APIRouter(tags=["认证模块"])

# 统一定义登录失败异常，减少重复代码
AUTH_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="用户名或密码错误",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    用户名密码登录
    """
    # 校验逻辑
    if not verify_admin_credentials(login_data.username, login_data.password):
        raise AUTH_EXCEPTION

    # 签发令牌
    access_token = create_access_token(data={"sub": login_data.username})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",  # 明确返回 token 类型
        username=login_data.username
    )


@router.post("/login/swagger", include_in_schema=False)
async def login_for_swagger(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    专门给 Swagger UI 使用的登录接口
    """
    if not verify_admin_credentials(form_data.username, form_data.password):
        raise AUTH_EXCEPTION

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/access-key", response_model=TokenResponse)
async def login_with_access_key(login_data: AccessKeyLoginRequest):
    """AccessKey快速登录"""
    if not verify_access_key(login_data.access_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="AccessKey无效"
        )

    access_token = create_access_token(data={"sub": settings.admin_username})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        username=settings.admin_username
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout(_: UserInfo = Depends(get_current_user)):
    """
    退出登录 (JWT 无状态模式下，后端主要是清除前端缓存，
    若需真正注销需引入 Redis 黑名单)
    """
    return LogoutResponse(message="退出登录成功")


@router.get("/user/info", response_model=UserInfo)
async def get_user_info(current_user: UserInfo = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user


@router.get("/dashboard")
async def get_dashboard(current_user: UserInfo = Depends(get_current_user)):
    """仪表板数据 (受保护接口)"""
    return {
        "message": f"欢迎 {current_user.username}",
        "stats": {
            "total_users": 100,
            "active_users": 85,
            "total_orders": 1250,
            "revenue": 50000
        }
    }