import os
import json
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field, root_validator

from auth.auth import get_current_user
from models import UserInfo

# --- 1. 模型定义（含自动校验） ---

class ContentItem(BaseModel):
    title: str = Field(..., min_length=1)
    text: str = Field(...)

class ContentBlock(BaseModel):
    type: str
    title: str = Field(..., min_length=1)
    subtitle: Optional[str] = ""
    items: List[ContentItem] = []

    @root_validator(skip_on_failure=True)
    def check_items_requirement(cls, values):
        """业务校验：特定类型必须包含 items"""
        b_type = values.get("type")
        items = values.get("items")
        if b_type in ['origin', 'mission', 'timeline'] and not items:
            raise ValueError(f"类型为 {b_type} 时，内容项(items)不能为空")
        return values

class AboutConfig(BaseModel):
    content: List[ContentBlock]

# --- 2. 逻辑层：配置管理 ---

class ConfigManager:
    def __init__(self):
        # 统一路径管理
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path = os.path.join(base_dir, "config", "关于我们", "config.json")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    async def read(self) -> dict:
        if not os.path.exists(self.path):
            return {"content": []}
        async with aiofiles.open(self.path, mode='r', encoding='utf-8') as f:
            try:
                content = await f.read()
                return json.loads(content)
            except json.JSONDecodeError:
                return {"content": []}

    async def write(self, data: dict):
        async with aiofiles.open(self.path, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))

config_manager = ConfigManager()
router = APIRouter(prefix="/about", tags=["关于我们管理"])

# --- 3. 路由接口 ---

@router.get("/config", response_model=AboutConfig)
async def get_about_config(_: UserInfo = Depends(get_current_user)):
    """获取配置（异步非阻塞）"""
    return await config_manager.read()

@router.put("/config")
async def update_about_config(
    config: AboutConfig, 
    _: UserInfo = Depends(get_current_user)
):
    """更新配置（利用 Pydantic 自动校验）"""
    try:
        await config_manager.write(config.dict())
        return {"message": "配置更新成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"写入文件失败: {str(e)}"
        )