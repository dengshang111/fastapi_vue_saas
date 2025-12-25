import os
import json
import aiofiles
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

from auth.auth import get_current_user
from models import UserInfo


# --- 1. 数据模型 ---

class ContentImage(BaseModel):
    image: str = Field(..., description="图片URL或路径")


class ContentItem(BaseModel):
    coverTitle: str = Field(..., min_length=1)
    coverTag: str = Field(...)
    subTitle: str = Field(...)
    coverImage: str = Field(..., description="封面图地址")
    linkUrl: str = Field("", description="跳转链接")
    images: List[ContentImage] = []


class ContentConfig(BaseModel):
    items: List[ContentItem] = []


# --- 2. 配置管理服务 ---

class ContentService:
    def __init__(self):
        # 路径配置
        self.base_dir = Path(__file__).parent.parent
        self.config_path = self.base_dir / "config" / "企业内容" / "config.json"
        self.upload_dir = Path("uploads")

        # 确保目录存在
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def load(self) -> dict:
        """异步加载配置"""
        if not self.config_path.exists():
            return {"items": []}
        try:
            async with aiofiles.open(self.config_path, mode='r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
        except (json.JSONDecodeError, Exception):
            return {"items": []}

    async def save(self, data: dict):
        """异步保存配置"""
        async with aiofiles.open(self.config_path, mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))

    def check_image_exists(self, url: str) -> bool:
        """
        验证图片物理文件是否存在
        支持从 URL '/api/upload/static/filename' 提取文件名
        """
        if not url:
            return False
        # 提取文件名：取 URL 路径的最后一部分
        filename = Path(url).name
        file_path = self.upload_dir / filename
        return file_path.exists()


content_service = ContentService()
router = APIRouter(prefix="/content", tags=["企业内容管理"])


# --- 3. 路由接口 ---

@router.get("/config", response_model=ContentConfig)
async def get_content_config(_: UserInfo = Depends(get_current_user)):
    """获取企业内容配置"""
    return await content_service.load()


@router.put("/config")
async def update_content_config(
        config: ContentConfig,
        _: UserInfo = Depends(get_current_user)
):
    """更新企业内容配置"""
    # 1. 业务逻辑校验：图片存在性检查
    for item in config.items:
        # 检查封面
        if not content_service.check_image_exists(item.coverImage):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"封面图文件不存在: {item.coverImage}"
            )

        # 检查详情图列表
        for img_obj in item.images:
            if not content_service.check_image_exists(img_obj.image):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"详情图文件不存在: {img_obj.image}"
                )

    # 2. 持久化存储
    try:
        await content_service.save(config.dict())
        return {"message": "配置更新成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存配置失败: {str(e)}"
        )