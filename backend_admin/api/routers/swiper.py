import os
import json
import aiofiles
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from auth.auth import get_current_user
from models import UserInfo


# --- 1. 数据模型 ---

class SwiperImage(BaseModel):
    title: str = Field("", description="图片标题/描述")
    image: str = Field(..., description="图片URL或相对路径")


class SwiperConfig(BaseModel):
    images: List[SwiperImage] = []


# --- 2. 配置管理服务 ---

class SwiperService:
    def __init__(self):
        # 使用 pathlib 保证跨平台路径兼容性
        self.base_dir = Path(__file__).parent.parent
        self.config_path = self.base_dir / "config" / "轮播图" / "config.json"
        self.upload_dir = Path("uploads")

        # 确保初始化时目录存在
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def load(self) -> dict:
        """异步加载轮播图配置"""
        if not self.config_path.exists():
            return {"images": []}
        try:
            async with aiofiles.open(self.config_path, mode='r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except (json.JSONDecodeError, Exception):
            return {"images": []}

    async def save(self, data: dict):
        """异步保存轮播图配置"""
        async with aiofiles.open(self.config_path, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))

    def verify_image(self, url: str) -> bool:
        """解析URL并检查物理文件是否存在"""
        if not url:
            return False
        # 无论URL前缀如何，提取最后的文件名进行校验
        filename = Path(url).name
        return (self.upload_dir / filename).exists()


swiper_service = SwiperService()
router = APIRouter(prefix="/swiper", tags=["轮播图管理"])


# --- 3. 路由接口 ---

@router.get("/config", response_model=SwiperConfig)
async def get_swiper_config(_: UserInfo = Depends(get_current_user)):
    """获取轮播图配置"""
    return await swiper_service.load()


@router.put("/config")
async def update_swiper_config(
        config: SwiperConfig,
        _: UserInfo = Depends(get_current_user)
):
    """更新轮播图配置并校验图片"""
    # 1. 物理文件存在性校验
    for item in config.images:
        if not swiper_service.verify_image(item.image):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"轮播图片物理文件不存在: {item.image}"
            )

    # 2. 异步持久化
    try:
        await swiper_service.save(config.dict())
        return {"message": "轮播图配置更新成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存配置失败: {str(e)}"
        )