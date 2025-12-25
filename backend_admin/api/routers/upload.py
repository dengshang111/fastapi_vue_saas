import os
import uuid
import shutil
import aiofiles
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse, Response
from PIL import Image
from pydantic import BaseModel

from auth.auth import get_current_user
from models import UserInfo, LogoutResponse
from configs.config import settings

router = APIRouter(prefix="/api/upload", tags=["文件上传系统"])

# --- 配置中心 ---
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
THUMB_DIR = UPLOAD_DIR / ".thumbnails"  # 缩略图缓存目录
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

class BatchDeleteRequest(BaseModel):
    """批量删除请求体"""
    filenames: List[str]

# 确保目录存在
for d in [UPLOAD_DIR, THUMB_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# --- 工具函数 ---

async def save_file_async(file: UploadFile, destination: Path):
    """分块异步写入文件，保护内存"""
    async with aiofiles.open(destination, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # 每次读取 1MB
            await f.write(chunk)


def get_thumbnail_path(original_path: Path, size: str) -> Path:
    """生成缩略图缓存路径"""
    thumb_name = f"{original_path.stem}_{size}{original_path.suffix}"
    return THUMB_DIR / thumb_name


# --- 路由实现 ---

@router.post("/image")
async def upload_image(
        file: UploadFile = File(...),
        group: str = Form(""),
        _: UserInfo = Depends(get_current_user)
):
    """
    单图异步上传
    """
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "不支持的文件格式")

    # 确定目录
    target_dir = UPLOAD_DIR / group if group else UPLOAD_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    # 生成唯一文件名
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = target_dir / filename

    # 异步写入
    await save_file_async(file, file_path)

    # 简单的格式校验
    try:
        with Image.open(file_path) as img:
            img.verify()
    except:
        file_path.unlink()  # 删除非法文件
        raise HTTPException(400, "无效的图片文件")

    return {
        "filename": filename,
        "url": f"/api/upload/static/{group}/{filename}" if group else f"/api/upload/static/{filename}",
        "uploaded_at": datetime.now().isoformat()
    }


@router.get("/static/{file_path:path}")
async def get_static_file(
        file_path: str,
        token: str = "",
        thumbnail: Optional[str] = None
):
    """
    高性能静态文件访问，支持缩略图持久化缓存
    """
    if token != settings.secret_key:
        raise HTTPException(401, "未授权访问")

    original_path = (UPLOAD_DIR / file_path).resolve()

    # 安全性检查：防止 ../../ 攻击
    if not str(original_path).startswith(str(UPLOAD_DIR.resolve())):
        raise HTTPException(403, "拒绝访问")

    if not original_path.is_file():
        raise HTTPException(404, "文件不存在")

    # 缩略图逻辑优化
    if thumbnail:
        thumb_path = get_thumbnail_path(original_path, thumbnail)

        # 如果缓存存在直接返回，不经过 Pillow 处理
        if thumb_path.exists():
            return FileResponse(thumb_path)

        # 否则生成并缓存
        try:
            w, h = map(int, thumbnail.split('x')) if 'x' in thumbnail else (int(thumbnail), int(thumbnail))
            with Image.open(original_path) as img:
                img.thumbnail((w, h), Image.Resampling.LANCZOS)
                img.save(thumb_path, quality=85)
            return FileResponse(thumb_path)
        except:
            return FileResponse(original_path)

    return FileResponse(original_path)


@router.post("/batch-delete")
async def batch_delete(request: BatchDeleteRequest, _: UserInfo = Depends(get_current_user)):
    """
    批量删除并清理缩略图缓存
    """
    success, failed = [], []

    # 递归搜索文件
    for fname in request.filenames:
        found = False
        for p in UPLOAD_DIR.rglob(fname):  # 递归查找文件名匹配的文件
            try:
                # 1. 删除缩略图缓存
                for t in THUMB_DIR.glob(f"{p.stem}_*"):
                    t.unlink()
                # 2. 删除原图
                p.unlink()
                success.append(fname)
                found = True
                break
            except:
                pass

        if not found: failed.append(fname)

    return {"deleted": success, "failed": failed}


@router.get("/files")
async def list_files(group: str = "", _: UserInfo = Depends(get_current_user)):
    """
    获取文件列表（按时间排序）
    """
    target_dir = UPLOAD_DIR / group if group else UPLOAD_DIR
    if not target_dir.exists(): return []

    files_info = []
    for p in target_dir.iterdir():
        if p.is_file() and p.suffix.lower() in ALLOWED_EXTENSIONS:
            stat = p.stat()
            files_info.append({
                "filename": p.name,
                "url": f"/api/upload/static/{group}/{p.name}" if group else f"/api/upload/static/{p.name}",
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

    return sorted(files_info, key=lambda x: x['mtime'], reverse=True)