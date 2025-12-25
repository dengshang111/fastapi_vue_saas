import os
import json
import aiofiles
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, validator

from auth.auth import get_current_user
from models import UserInfo


# --- 1. 模型定义（强类型校验） ---

class SettingsConfig(BaseModel):
    # 使用 Literal 限制只能取这两个值，不符合会直接返回 422 错误
    theme: Literal["light", "dark"] = "light"
    autoSwitch: bool = False

    # 使用正则校验时间格式 HH:MM
    # ^([01]\d|2[0-3]):([0-5]\d)$ 确保小时 00-23，分钟 00-59
    darkModeTime: str = Field("18:00", regex=r"^([01]\d|2[0-3]):([0-5]\d)$")
    lightModeTime: str = Field("06:00", regex=r"^([01]\d|2[0-3]):([0-5]\d)$")


# --- 2. 配置管理服务 ---

class SettingsService:
    def __init__(self):
        # 路径优化
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(base_dir, "config", "系统设置", "config.json")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        # 默认配置对象
        self.default_data = {
            "theme": "light",
            "autoSwitch": False,
            "darkModeTime": "18:00",
            "lightModeTime": "06:00"
        }

    async def get_all(self) -> dict:
        if not os.path.exists(self.path):
            return self.default_data

        async with aiofiles.open(self.path, mode='r', encoding='utf-8') as f:
            try:
                content = await f.read()
                return {**self.default_data, **json.loads(content)}  # 合并默认值，防止字段缺失
            except (json.JSONDecodeError, Exception):
                return self.default_data

    async def update(self, data: dict):
        async with aiofiles.open(self.path, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))


settings_service = SettingsService()
router = APIRouter(prefix="/settings", tags=["系统设置"])


# --- 3. 路由接口 ---

@router.get("/config", response_model=SettingsConfig)
async def get_settings_config(_: UserInfo = Depends(get_current_user)):
    """获取系统设置"""
    return await settings_service.get_all()


@router.put("/config")
async def update_settings_config(
        config: SettingsConfig,
        _: UserInfo = Depends(get_current_user)
):
    """更新系统设置"""
    try:
        await settings_service.update(config.dict())
        return {"message": "设置更新成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"系统设置保存失败: {str(e)}"
        )