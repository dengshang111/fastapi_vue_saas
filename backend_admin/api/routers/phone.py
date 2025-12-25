import os
import json
import aiofiles
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from auth.auth import get_current_user
from models import UserInfo

# --- 1. 数据模型（声明式校验） ---

class PhoneConfig(BaseModel):
    # 使用正则表达式校验：1开头，后面跟10位数字
    phoneNumber: str = Field(
        ..., 
        pattern=r"^1[3-9]\d{9}$",
        description="11位中国大陆手机号码"
    )

# --- 2. 配置服务层 ---

class PhoneService:
    def __init__(self):
        # 使用 pathlib 处理路径，更具跨平台性
        base_dir = Path(__file__).parent.parent
        self.config_path = base_dir / "config" / "电话号码" / "config.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    async def load(self) -> dict:
        """异步加载配置"""
        if not self.config_path.exists():
            return {"phoneNumber": ""}
        try:
            async with aiofiles.open(self.config_path, mode='r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except (json.JSONDecodeError, Exception):
            return {"phoneNumber": ""}

    async def save(self, data: dict):
        """异步保存配置"""
        async with aiofiles.open(self.config_path, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))

phone_service = PhoneService()
router = APIRouter(prefix="/phone", tags=["电话号码管理"])

# --- 3. 路由接口 ---

@router.get("/config", response_model=PhoneConfig)
async def get_phone_config(_: UserInfo = Depends(get_current_user)):
    """获取电话号码配置"""
    return await phone_service.load()

@router.put("/config")
async def update_phone_config(
    config: PhoneConfig,
    _: UserInfo = Depends(get_current_user)
):
    """更新电话号码配置"""
    try:
        # 校验：由于在 PhoneConfig 中定义了 regex，格式不正确时 FastAPI 会自动返回 422 错误
        await phone_service.save(config.dict())
        return {"message": "电话号码配置更新成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存失败: {str(e)}"
        )