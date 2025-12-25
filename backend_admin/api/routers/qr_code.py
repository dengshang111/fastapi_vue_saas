import os
import json
import uuid
import aiofiles
from pathlib import Path
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from auth.auth import get_current_user
from models import UserInfo, TokenResponse  # 假设你有统一的响应基类
from pydantic import BaseModel, Field


# --- 1. 数据模型 ---

class QrCodeConfig(BaseModel):
    image: str = ""
    title: str = "小程序二维码"
    description: str = "扫描二维码体验小程序"
    enabled: bool = False


# --- 2. 逻辑服务层 ---

class QrCodeService:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.config_path = self.base_dir / "config" / "小程序二维码" / "config.json"
        self.upload_dir = self.base_dir / "uploads"

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def load(self) -> QrCodeConfig:
        if not self.config_path.exists():
            return QrCodeConfig()
        async with aiofiles.open(self.config_path, 'r', encoding='utf-8') as f:
            try:
                data = json.loads(await f.read())
                # 兼容旧代码的嵌套格式，如果是新格式则直接解析
                inner_data = data.get("qr_code", data) if isinstance(data, dict) else data
                return QrCodeConfig(**inner_data)
            except:
                return QrCodeConfig()

    async def save(self, config: QrCodeConfig):
        async with aiofiles.open(self.config_path, 'w', encoding='utf-8') as f:
            await f.write(config.json(ensure_ascii=False, indent=2))

    def delete_physical_file(self, url: str):
        """删除磁盘上的物理文件"""
        if not url: return
        filename = Path(url).name
        file_path = self.upload_dir / filename
        if file_path.exists():
            file_path.unlink()


qr_service = QrCodeService()
router = APIRouter(prefix="/qr-code", tags=["小程序二维码配置"])


# --- 3. 路由接口 ---

@router.get("/config", response_model=QrCodeConfig)
async def get_config(_: UserInfo = Depends(get_current_user)):
    return await qr_service.load()


@router.post("/upload")
async def upload_image(
        file: UploadFile = File(...),
        _: UserInfo = Depends(get_current_user)
):
    # 1. 验证格式
    ext = Path(file.filename).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(400, "不支持的图片格式")

    # 2. 异步保存文件
    unique_name = f"qr_{uuid.uuid4().hex}{ext}"
    file_path = qr_service.upload_dir / unique_name

    # 清理旧文件逻辑
    current_config = await qr_service.load()
    qr_service.delete_physical_file(current_config.image)

    # 分块读取写入，防止内存溢出
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(1024 * 1024):  # 每轮读 1MB
            await out_file.write(content)

    # 3. 更新配置
    new_url = f"/api/upload/static/{unique_name}"
    current_config.image = new_url
    current_config.enabled = True
    await qr_service.save(current_config)

    return {"url": new_url, "message": "上传成功"}


@router.put("/config")
async def update_config(
        update_data: QrCodeConfig,
        _: UserInfo = Depends(get_current_user)
):
    await qr_service.save(update_data)
    return {"message": "配置已更新"}


@router.delete("/image")
async def delete_image(_: UserInfo = Depends(get_current_user)):
    config = await qr_service.load()
    qr_service.delete_physical_file(config.image)
    config.image = ""
    config.enabled = False
    await qr_service.save(config)
    return {"message": "图片已清理"}


@router.get("/public")
async def get_public_config():
    """供移动端/小程序前端调用"""
    config = await qr_service.load()
    if not config.enabled or not config.image:
        return {"data": None}
    return {"data": config}