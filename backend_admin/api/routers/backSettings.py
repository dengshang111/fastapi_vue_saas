from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import json
import os

from auth.auth import get_current_user
from models import UserInfo

router = APIRouter(prefix="/api/settings", tags=["系统设置"])

# 数据模型
class SettingsConfig(BaseModel):
    theme: str = "light"
    autoSwitch: bool = False
    darkModeTime: str = "18:00"
    lightModeTime: str = "06:00"

# 数据文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "系统设置", "config.json")

# 确保数据目录存在
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

def load_config_data() -> dict:
    """加载config.json配置数据"""
    if not os.path.exists(CONFIG_FILE):
        # 初始化默认配置
        default_config = {
            "theme": "light",
            "autoSwitch": False,
            "darkModeTime": "18:00",
            "lightModeTime": "06:00"
        }
        save_config_data(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载config.json失败: {e}")
        return {
            "theme": "light",
            "autoSwitch": False,
            "darkModeTime": "18:00",
            "lightModeTime": "06:00"
        }

def save_config_data(data: dict):
    """保存config.json配置数据"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存config.json失败: {e}")

@router.get("/config", response_model=SettingsConfig)
async def get_settings_config(current_user: UserInfo = Depends(get_current_user)):
    """获取系统设置配置"""
    try:
        config_data = load_config_data()
        return config_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取系统设置配置失败: {str(e)}"
        )

@router.put("/config")
async def update_settings_config(
    config: SettingsConfig,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新系统设置配置"""
    try:
        # 验证主题模式
        if config.theme not in ["light", "dark"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="主题模式必须是 'light' 或 'dark'"
            )
        
        # 验证时间格式
        try:
            # 验证时间格式 (HH:MM)
            if not (len(config.darkModeTime) == 5 and 
                   config.darkModeTime[2] == ':' and
                   config.darkModeTime[:2].isdigit() and 
                   config.darkModeTime[3:].isdigit() and
                   0 <= int(config.darkModeTime[:2]) <= 23 and
                   0 <= int(config.darkModeTime[3:]) <= 59):
                raise ValueError("深色模式时间格式错误")
            
            if not (len(config.lightModeTime) == 5 and 
                   config.lightModeTime[2] == ':' and
                   config.lightModeTime[:2].isdigit() and 
                   config.lightModeTime[3:].isdigit() and
                   0 <= int(config.lightModeTime[:2]) <= 23 and
                   0 <= int(config.lightModeTime[3:]) <= 59):
                raise ValueError("浅色模式时间格式错误")
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"时间格式错误: {str(e)}"
            )
        
        # 保存配置
        save_config_data(config.dict())
        
        return {"message": "设置更新成功"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新系统设置配置失败: {str(e)}"
        ) 