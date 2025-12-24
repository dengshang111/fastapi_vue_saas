from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import json
import os

from auth.auth import get_current_user
from models import UserInfo

router = APIRouter(prefix="/api/phone", tags=["电话号码管理"])

# 数据模型
class PhoneConfig(BaseModel):
    phoneNumber: str

# 数据文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "电话号码", "config.json")

# 确保数据目录存在
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

def load_config_data() -> dict:
    """加载config.json配置数据"""
    if not os.path.exists(CONFIG_FILE):
        # 初始化默认配置
        default_config = {"phoneNumber": ""}
        save_config_data(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载config.json失败: {e}")
        return {"phoneNumber": ""}

def save_config_data(data: dict):
    """保存config.json配置数据"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存config.json失败: {e}")

@router.get("/config", response_model=PhoneConfig)
async def get_phone_config(current_user: UserInfo = Depends(get_current_user)):
    """获取电话号码配置"""
    try:
        config_data = load_config_data()
        return config_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取电话号码配置失败: {str(e)}"
        )

@router.put("/config")
async def update_phone_config(
    config: PhoneConfig,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新电话号码配置"""
    try:
        # 验证电话号码格式
        if not config.phoneNumber.isdigit() or len(config.phoneNumber) != 11:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请输入正确的11位手机号码"
            )
        
        # 保存配置
        save_config_data(config.dict())
        
        return {"message": "配置更新成功"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新电话号码配置失败: {str(e)}"
        ) 