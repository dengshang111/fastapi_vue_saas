from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import json
import os
from datetime import datetime

from auth import get_current_user
from models import UserInfo

router = APIRouter(prefix="/api/swiper", tags=["轮播图管理"])

# 数据模型
class SwiperImage(BaseModel):
    title: str = ""
    image: str

class SwiperConfig(BaseModel):
    images: List[SwiperImage]

# 数据文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "轮播图", "config.json")
UPLOAD_DIR = "uploads"

# 确保数据目录存在
os.makedirs("data", exist_ok=True)
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_config_data() -> dict:
    """加载config.json配置数据"""
    if not os.path.exists(CONFIG_FILE):
        # 初始化默认配置
        default_config = {"images": []}
        save_config_data(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载config.json失败: {e}")
        return {"images": []}

def save_config_data(data: dict):
    """保存config.json配置数据"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存config.json失败: {e}")

@router.get("/config", response_model=SwiperConfig)
async def get_swiper_config(current_user: UserInfo = Depends(get_current_user)):
    """获取轮播图配置"""
    try:
        config_data = load_config_data()
        return config_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取轮播图配置失败: {str(e)}"
        )

@router.put("/config")
async def update_swiper_config(
    config: SwiperConfig,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新轮播图配置"""
    try:
        # 验证所有图片路径是否存在
        for item in config.images:
            # 从图片URL中提取路径信息
            # URL格式可能是: /api/upload/static/filename 或 /api/upload/static/group/filename
            image_url = item.image
            
            # 移除URL前缀，获取相对路径
            if image_url.startswith("/api/upload/static/"):
                relative_path = image_url[len("/api/upload/static/"):]
            else:
                # 如果不是标准URL格式，尝试直接使用文件名
                relative_path = os.path.basename(image_url)
            
            # 构建完整的文件路径
            image_path = os.path.join(UPLOAD_DIR, relative_path)
            
            # 检查文件是否存在
            if not os.path.exists(image_path):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"图片不存在: {item.image}"
                )
        
        # 保存配置
        save_config_data(config.dict())
        
        return {"message": "配置更新成功"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新轮播图配置失败: {str(e)}"
        )

