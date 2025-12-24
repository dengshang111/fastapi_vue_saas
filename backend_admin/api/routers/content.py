from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from typing import List
import json
import os

from auth.auth import get_current_user
from models import UserInfo

router = APIRouter(prefix="/api/content", tags=["企业内容管理"])

# 数据模型
class ContentImage(BaseModel):
    """内容图片"""
    image: str

class ContentItem(BaseModel):
    """企业内容项"""
    coverTitle: str
    coverTag: str
    subTitle: str
    coverImage: str
    linkUrl: str
    images: List[ContentImage] = []

class ContentConfig(BaseModel):
    """企业内容配置"""
    items: List[ContentItem] = []

# 数据文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "企业内容", "config.json")
UPLOAD_DIR = "uploads"

# 确保数据目录存在
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_config_data() -> dict:
    """加载config.json配置数据"""
    if not os.path.exists(CONFIG_FILE):
        # 初始化默认配置
        default_config = {"items": []}
        save_config_data(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载config.json失败: {e}")
        return {"items": []}

def save_config_data(data: dict):
    """保存config.json配置数据"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存config.json失败: {e}")

@router.get("/config", response_model=ContentConfig)
async def get_content_config(current_user: UserInfo = Depends(get_current_user)):
    """获取企业内容配置"""
    try:
        config_data = load_config_data()
        return config_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业内容配置失败: {str(e)}"
        )

@router.put("/config")
async def update_content_config(
    config: ContentConfig,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新企业内容配置"""
    try:
        # 验证所有图片路径是否存在
        for item in config.items:
            # 验证封面图
            cover_image_url = item.coverImage
            # 从图片URL中提取路径信息
            # URL格式可能是: /api/upload/static/filename 或 /api/upload/static/group/filename
            if cover_image_url.startswith("/api/upload/static/"):
                cover_relative_path = cover_image_url[len("/api/upload/static/"):]
            else:
                # 如果不是标准URL格式，尝试直接使用文件名
                cover_relative_path = os.path.basename(cover_image_url)
            
            cover_image_path = os.path.join(UPLOAD_DIR, cover_relative_path)
            if not os.path.exists(cover_image_path):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"封面图片不存在: {item.coverImage}"
                )
            
            # 验证内容图片
            for img in item.images:
                image_url = img.image
                # 从图片URL中提取路径信息
                if image_url.startswith("/api/upload/static/"):
                    relative_path = image_url[len("/api/upload/static/"):]
                else:
                    # 如果不是标准URL格式，尝试直接使用文件名
                    relative_path = os.path.basename(image_url)
                
                image_path = os.path.join(UPLOAD_DIR, relative_path)
                if not os.path.exists(image_path):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"内容图片不存在: {img.image}"
                    )
        
        # 保存配置
        save_config_data(config.dict())
        
        return {"message": "配置更新成功"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新企业内容配置失败: {str(e)}"
        ) 