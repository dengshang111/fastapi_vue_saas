from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import os

from auth.auth import get_current_user
from models import UserInfo

router = APIRouter(prefix="/api/about", tags=["关于我们管理"])

# 数据模型
class ContentItem(BaseModel):
    title: str
    text: str

class ContentBlock(BaseModel):
    type: str
    title: str
    subtitle: Optional[str] = ""
    items: Optional[List[ContentItem]] = []

class AboutConfig(BaseModel):
    content: List[ContentBlock]

# 数据文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "关于我们", "config.json")

# 确保数据目录存在
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

def load_config_data() -> dict:
    """加载config.json配置数据"""
    if not os.path.exists(CONFIG_FILE):
        # 初始化默认配置
        default_config = {"content": []}
        save_config_data(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载config.json失败: {e}")
        return {"content": []}

def save_config_data(data: dict):
    """保存config.json配置数据"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存config.json失败: {e}")

@router.get("/config", response_model=AboutConfig)
async def get_about_config(current_user: UserInfo = Depends(get_current_user)):
    """获取关于我们配置"""
    try:
        config_data = load_config_data()
        return config_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取关于我们配置失败: {str(e)}"
        )

@router.put("/config")
async def update_about_config(
    config: AboutConfig,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新关于我们配置"""
    try:
        # 验证内容结构
        for block in config.content:
            if not block.type or not block.title:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="内容块必须包含类型和标题"
                )
            
            # 验证需要items的内容块
            if block.type in ['origin', 'mission', 'timeline'] and not block.items:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{block.type}类型的内容块必须包含内容项"
                )
        
        # 保存配置
        save_config_data(config.dict())
        
        return {"message": "配置更新成功"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新关于我们配置失败: {str(e)}"
        ) 