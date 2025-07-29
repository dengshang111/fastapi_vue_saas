from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional
import os
import json
from pydantic import BaseModel

from auth import get_current_user
from models import UserInfo
from config import settings

# 请求模型
class QrCodeConfig(BaseModel):
    image: str = ""
    title: str = "小程序二维码"
    description: str = "扫描二维码体验小程序"
    enabled: bool = False

class QrCodeUpdateRequest(BaseModel):
    image: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None

router = APIRouter(prefix="/api/qr-code", tags=["小程序二维码配置"])

# 配置文件路径
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "小程序二维码")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# 确保配置目录存在
os.makedirs(CONFIG_DIR, exist_ok=True)

def load_qr_code_config() -> dict:
    """加载小程序二维码配置"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 创建默认配置
            default_config = {
                "qr_code": {
                    "image": "",
                    "title": "小程序二维码",
                    "description": "扫描二维码体验小程序",
                    "enabled": False
                }
            }
            save_qr_code_config(default_config)
            return default_config
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"加载配置失败: {str(e)}"
        )

def save_qr_code_config(config: dict):
    """保存小程序二维码配置"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存配置失败: {str(e)}"
        )

@router.get("/config")
async def get_qr_code_config(current_user: UserInfo = Depends(get_current_user)):
    """获取小程序二维码配置"""
    try:
        config = load_qr_code_config()
        return {
            "success": True,
            "data": config.get("qr_code", {}),
            "message": "获取配置成功"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取配置失败: {str(e)}"
        )

@router.post("/upload")
async def upload_qr_code_image(
    file: UploadFile = File(...),
    current_user: UserInfo = Depends(get_current_user)
):
    """上传小程序二维码图片"""
    try:
        # 检查文件名
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件名不能为空"
            )
        
        # 检查文件类型
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只支持 JPG, PNG, GIF, WebP 格式的图片"
            )
        
        # 检查文件大小（最大5MB）
        content = file.file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="文件大小超过限制（最大5MB）"
            )
        
        # 保存到uploads目录
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成唯一文件名
        import uuid
        unique_filename = f"qr_code_{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 更新配置
        config = load_qr_code_config()
        config["qr_code"]["image"] = f"/api/upload/static/{unique_filename}"
        save_qr_code_config(config)
        
        return {
            "success": True,
            "data": {
                "filename": unique_filename,
                "url": f"/api/upload/static/{unique_filename}",
                "size": len(content)
            },
            "message": "二维码图片上传成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败: {str(e)}"
        )

@router.put("/config")
async def update_qr_code_config(
    request: QrCodeUpdateRequest,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新小程序二维码配置"""
    try:
        config = load_qr_code_config()
        qr_code_config = config.get("qr_code", {})
        
        # 更新配置
        if request.image is not None:
            qr_code_config["image"] = request.image
        if request.title is not None:
            qr_code_config["title"] = request.title
        if request.description is not None:
            qr_code_config["description"] = request.description
        if request.enabled is not None:
            qr_code_config["enabled"] = request.enabled
        
        config["qr_code"] = qr_code_config
        save_qr_code_config(config)
        
        return {
            "success": True,
            "data": qr_code_config,
            "message": "配置更新成功"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新配置失败: {str(e)}"
        )

@router.delete("/image")
async def delete_qr_code_image(current_user: UserInfo = Depends(get_current_user)):
    """删除小程序二维码图片"""
    try:
        config = load_qr_code_config()
        qr_code_config = config.get("qr_code", {})
        
        # 清除图片配置
        qr_code_config["image"] = ""
        qr_code_config["enabled"] = False
        config["qr_code"] = qr_code_config
        save_qr_code_config(config)
        
        return {
            "success": True,
            "message": "二维码图片已删除"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败: {str(e)}"
        )

@router.get("/public")
async def get_public_qr_code_config():
    """获取公开的小程序二维码配置（无需认证）"""
    try:
        config = load_qr_code_config()
        qr_code_config = config.get("qr_code", {})
        
        # 只返回启用的配置
        if qr_code_config.get("enabled", False) and qr_code_config.get("image"):
            return {
                "success": True,
                "data": {
                    "image": qr_code_config.get("image", ""),
                    "title": qr_code_config.get("title", "小程序二维码"),
                    "description": qr_code_config.get("description", "扫描二维码体验小程序")
                }
            }
        else:
            return {
                "success": True,
                "data": None,
                "message": "未配置小程序二维码"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取配置失败: {str(e)}"
        ) 