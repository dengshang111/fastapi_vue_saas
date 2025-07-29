from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse, Response
from typing import List, Optional
import os
import uuid
from datetime import datetime
from PIL import Image
import io
import shutil
from pydantic import BaseModel

from auth import get_current_user
from models import UserInfo
from config import settings

# 请求模型
class GroupCreate(BaseModel):
    name: str

class BatchDeleteRequest(BaseModel):
    filenames: List[str]

router = APIRouter(prefix="/api/upload", tags=["文件上传"])

# 上传目录配置
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# 访问密钥
ACCESS_KEY = settings.secret_key

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

def is_valid_image_file(filename: str) -> bool:
    """检查是否为有效的图片文件"""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

def generate_thumbnail(file_path: str, width: int, height: int) -> bytes:
    """生成缩略图并返回字节数据"""
    with Image.open(file_path) as img:
        # 保持EXIF方向信息
        try:
            exif = img.getexif()
            orientation = exif.get(274)  # EXIF orientation tag
            if orientation:
                # 根据EXIF方向旋转图片
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        except Exception:
            # 如果EXIF读取失败，继续处理
            pass
        
        # 保持宽高比
        img.thumbnail((width, height), Image.Resampling.LANCZOS)
        
        # 将缩略图保存到内存
        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format=img.format or 'JPEG', quality=85)
        buffer.seek(0)
        
        # 获取buffer内容并立即释放内存
        content = buffer.getvalue()
        buffer.close()
        
        return content

def save_uploaded_image(file: UploadFile, group: str = "") -> str:
    """保存上传的图片文件"""
    try:
        # 检查文件名
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件名不能为空"
            )
        
        # 读取文件内容
        content = file.file.read()
        
        # 检查文件大小
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="文件大小超过限制（最大10MB）"
            )
        
        # 验证图片格式
        try:
            image = Image.open(io.BytesIO(content))
            image.verify()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的图片文件"
            )
        
        # 确定保存路径
        if group:
            group_dir = os.path.join(UPLOAD_DIR, group)
            os.makedirs(group_dir, exist_ok=True)
            save_dir = group_dir
        else:
            save_dir = UPLOAD_DIR
        
        # 生成唯一文件名
        file_extension = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(save_dir, unique_filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(content)
        
        return unique_filename
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    group: Optional[str] = Form(""),
    current_user: UserInfo = Depends(get_current_user)
):
    """上传图片文件"""
    # 检查文件名
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件名不能为空"
        )
    
    # 检查文件类型
    if not is_valid_image_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持 JPG, PNG, GIF, WebP 格式的图片"
        )
    
    # 读取文件内容以获取大小
    content = file.file.read()
    file.file.seek(0)  # 重置文件指针
    
    # 保存文件
    filename = save_uploaded_image(file, group or "")
    
    # 返回文件信息
    return {
        "filename": filename,
        "original_name": file.filename,
        "url": f"/api/upload/image/{group}/{filename}" if group else f"/api/upload/image/{filename}",
        "size": len(content),
        "uploaded_at": datetime.now().isoformat(),
        "group": group
    }

@router.post("/batch-upload")
async def batch_upload_images(
    files: List[UploadFile] = File(...),
    group: Optional[str] = Form(""),
    current_user: UserInfo = Depends(get_current_user)
):
    """批量上传图片文件"""
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请选择要上传的文件"
        )
    
    results = []
    errors = []
    
    for file in files:
        try:
            # 检查文件名
            if not file.filename:
                errors.append({"filename": "未知文件", "error": "文件名不能为空"})
                continue
            
            # 检查文件类型
            if not is_valid_image_file(file.filename):
                errors.append({"filename": file.filename, "error": "只支持 JPG, PNG, GIF, WebP 格式的图片"})
                continue
            
            # 读取文件内容以获取大小
            content = file.file.read()
            file.file.seek(0)  # 重置文件指针
            
            # 检查文件大小
            if len(content) > MAX_FILE_SIZE:
                errors.append({"filename": file.filename, "error": "文件大小超过限制（最大10MB）"})
                continue
            
            # 保存文件
            filename = save_uploaded_image(file, group or "")
            
            # 添加到成功结果
            results.append({
                "filename": filename,
                "original_name": file.filename,
                "url": f"/api/upload/static/{group}/{filename}" if group else f"/api/upload/static/{filename}",
                "size": len(content),
                "uploaded_at": datetime.now().isoformat(),
                "group": group
            })
            
        except Exception as e:
            errors.append({"filename": file.filename or "未知文件", "error": str(e)})
    
    return {
        "success_count": len(results),
        "error_count": len(errors),
        "results": results,
        "errors": errors,
        "message": f"成功上传 {len(results)} 个文件，失败 {len(errors)} 个文件"
    }

@router.get("/files")
async def get_files(
    group: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """获取文件列表"""
    try:
        files = []
        
        if group:
            # 获取指定分组的文件
            group_dir = os.path.join(UPLOAD_DIR, group)
            if not os.path.exists(group_dir):
                return []
            
            for filename in os.listdir(group_dir):
                if is_valid_image_file(filename):
                    file_path = os.path.join(group_dir, filename)
                    file_stat = os.stat(file_path)
                    files.append({
                        "filename": filename,
                        "url": f"/api/upload/static/{group}/{filename}",
                        "size": file_stat.st_size,
                        "uploaded_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        "group": group
                    })
        else:
            # 获取默认分组的文件
            for filename in os.listdir(UPLOAD_DIR):
                if is_valid_image_file(filename):
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    file_stat = os.stat(file_path)
                    files.append({
                        "filename": filename,
                        "url": f"/api/upload/static/{filename}",
                        "size": file_stat.st_size,
                        "uploaded_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        "group": ""
                    })
        
        # 按上传时间倒序排列
        files.sort(key=lambda x: x["uploaded_at"], reverse=True)
        return files
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件列表失败: {str(e)}"
        )

@router.get("/groups")
async def get_groups(current_user: UserInfo = Depends(get_current_user)):
    """获取分组列表"""
    try:
        groups = []
        
        # 获取所有子目录作为分组
        for item in os.listdir(UPLOAD_DIR):
            item_path = os.path.join(UPLOAD_DIR, item)
            if os.path.isdir(item_path):
                # 计算分组中的文件数量
                file_count = 0
                for filename in os.listdir(item_path):
                    if is_valid_image_file(filename):
                        file_count += 1
                
                groups.append({
                    "name": item,
                    "file_count": file_count
                })
        
        return groups
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取分组列表失败: {str(e)}"
        )

@router.post("/groups")
async def create_group(
    group_data: GroupCreate,
    current_user: UserInfo = Depends(get_current_user)
):
    """创建分组"""
    try:
        group_name = group_data.name.strip()
        if not group_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分组名称不能为空"
            )
        
        group_dir = os.path.join(UPLOAD_DIR, group_name)
        if os.path.exists(group_dir):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分组已存在"
            )
        
        os.makedirs(group_dir, exist_ok=True)
        
        return {
            "name": group_name,
            "message": "分组创建成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建分组失败: {str(e)}"
        )

@router.delete("/groups/{group_name}")
async def delete_group(
    group_name: str,
    current_user: UserInfo = Depends(get_current_user)
):
    
    """删除分组，分组必须为空才能删除"""
    try:
        group_dir = os.path.join(UPLOAD_DIR, group_name)
        if not os.path.exists(group_dir):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="分组不存在"
            )
        # 检查分组下是否有图片文件
        for filename in os.listdir(group_dir):
            if is_valid_image_file(filename):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="分组不为空，无法删除"
                )
        # 删除分组目录
        shutil.rmtree(group_dir)
        return {
            "message": f"分组 '{group_name}' 删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除分组失败: {str(e)}"
        )

@router.post("/batch-delete")
async def batch_delete_files(
    request: BatchDeleteRequest,
    current_user: UserInfo = Depends(get_current_user)
):
    """批量删除文件"""
    try:
        deleted_files = []
        failed_files = []
        
        for filename in request.filenames:
            try:
                # 尝试在默认目录删除
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
                    continue
                
                # 尝试在各个分组目录中查找并删除
                for group_name in os.listdir(UPLOAD_DIR):
                    group_path = os.path.join(UPLOAD_DIR, group_name)
                    if os.path.isdir(group_path):
                        group_file_path = os.path.join(group_path, filename)
                        if os.path.exists(group_file_path):
                            os.remove(group_file_path)
                            deleted_files.append(filename)
                            break
                else:
                    failed_files.append(filename)
                    
            except Exception as e:
                failed_files.append(filename)
                print(f"删除文件 {filename} 失败: {str(e)}")
        
        return {
            "deleted_files": deleted_files,
            "failed_files": failed_files,
            "message": f"成功删除 {len(deleted_files)} 个文件，失败 {len(failed_files)} 个文件"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量删除失败: {str(e)}"
        )

@router.delete("/image/{group}/{filename}")
async def delete_image_in_group(
    group: str,
    filename: str,
    current_user: UserInfo = Depends(get_current_user)
):
    """删除分组中的图片"""
    file_path = os.path.join(UPLOAD_DIR, group, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    try:
        os.remove(file_path)
        return {"message": "文件删除成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件删除失败: {str(e)}"
        )

@router.delete("/image/{filename}")
async def delete_image(
    filename: str,
    current_user: UserInfo = Depends(get_current_user)
):
    """删除默认分组中的图片"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    try:
        os.remove(file_path)
        return {"message": "文件删除成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件删除失败: {str(e)}"
        )

@router.get("/static/{file_path:path}")
async def static_file(file_path: str, token: str = "", thumbnail: Optional[str] = None):
    """带token验证的静态文件访问，支持缩略图生成"""
    # 校验token
    if token != ACCESS_KEY:
        raise HTTPException(status_code=401, detail="无效的token")

    # 构建完整文件路径
    abs_path = os.path.abspath(os.path.join(UPLOAD_DIR, file_path))
    if not abs_path.startswith(UPLOAD_DIR):
        raise HTTPException(status_code=403, detail="禁止访问")
    if not os.path.isfile(abs_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    # 如果请求缩略图，则生成缩略图
    if thumbnail and is_valid_image_file(file_path):
        try:
            # 解析缩略图尺寸参数，例如 "300x300"
            if 'x' in thumbnail:
                width, height = map(int, thumbnail.split('x'))
            else:
                width = height = int(thumbnail)
            
            # 生成缩略图
            content = generate_thumbnail(abs_path, width, height)
            # 获取图片格式
            with Image.open(abs_path) as img:
                img_format = img.format.lower() if img.format else 'jpeg'
            return Response(
                content=content,
                media_type=f"image/{img_format}"
            )
        except Exception as e:
            # 如果缩略图生成失败，返回原图
            print(f"缩略图生成失败: {e}")
            return FileResponse(abs_path)

    return FileResponse(abs_path) 