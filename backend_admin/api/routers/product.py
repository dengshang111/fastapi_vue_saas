import json
import uuid
import aiofiles
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from auth.auth import get_current_user
from models import UserInfo


# --- 1. 数据模型 ---

class Category(BaseModel):
    name: str = Field(..., min_length=1)
    key: str = Field(..., description="唯一代码，如 CY")


class Product(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., min_length=1)
    category: str = Field(..., description="关联分类的 key")
    description: str = ""
    mainImage: str = Field(..., description="主图URL")
    images: List[str] = Field(default=[], description="详情图列表")


# 统一响应包装
class CategoryResponse(BaseModel):
    categories: List[Category]


class ProductResponse(BaseModel):
    products: List[Product]


# --- 2. 核心服务层 ---

class ProductService:
    def __init__(self):
        base_path = Path(__file__).parent.parent / "config" / "产品"
        base_path.mkdir(parents=True, exist_ok=True)
        self.cat_file = base_path / "categories.json"
        self.prod_file = base_path / "products.json"
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def _read_file(self, path: Path) -> List:
        if not path.exists(): return []
        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            try:
                return json.loads(await f.read())
            except:
                return []

    async def _write_file(self, path: Path, data: List):
        async with aiofiles.open(path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))

    def check_file_exists(self, url: str) -> bool:
        """解析URL并检查物理文件是否存在"""
        if not url: return False
        filename = Path(url).name
        return (self.upload_dir / filename).exists()


service = ProductService()
router = APIRouter(prefix="/product", tags=["产品管理"])


# --- 3. 分类路由 ---

@router.get("/categories", response_model=CategoryResponse)
async def get_categories(_: UserInfo = Depends(get_current_user)):
    return {"categories": await service._read_file(service.cat_file)}


@router.post("/categories", response_model=Category)
async def add_category(cat: Category, _: UserInfo = Depends(get_current_user)):
    cats = await service._read_file(service.cat_file)
    if any(c['key'] == cat.key for c in cats):
        raise HTTPException(400, "分类代码已存在")
    cats.append(cat.dict())
    await service._write_file(service.cat_file, cats)
    return cat


@router.delete("/categories/{key}")
async def remove_category(key: str, _: UserInfo = Depends(get_current_user)):
    cats = await service._read_file(service.cat_file)
    prods = await service._read_file(service.prod_file)

    # 完整性校验
    if any(p['category'] == key for p in prods):
        raise HTTPException(400, "该分类下尚有产品，无法删除")

    new_cats = [c for c in cats if c['key'] != key]
    if len(new_cats) == len(cats):
        raise HTTPException(404, "分类不存在")

    await service._write_file(service.cat_file, new_cats)
    return {"message": "删除成功"}


# --- 4. 产品路由 ---

@router.get("/list", response_model=ProductResponse)
async def list_products(category: str = "all", _: UserInfo = Depends(get_current_user)):
    prods = await service._read_file(service.prod_file)
    if category != "all":
        prods = [p for p in prods if p['category'] == category]
    return {"products": prods}


@router.post("/new", response_model=Product)
async def add_product(prod: Product, _: UserInfo = Depends(get_current_user)):
    # 1. 验证分类
    cats = await service._read_file(service.cat_file)
    if not any(c['key'] == prod.category for c in cats):
        raise HTTPException(400, "所属分类无效")

    # 2. 验证图片资源 (主图 + 详情图)
    all_images = [prod.mainImage] + prod.images
    for img_url in all_images:
        if not service.check_file_exists(img_url):
            raise HTTPException(400, f"图片文件不存在: {img_url}")

    # 3. 存储
    prods = await service._read_file(service.prod_file)
    new_prod = prod.dict()
    new_prod['id'] = uuid.uuid4().hex[:12]  # 生成短UUID
    prods.append(new_prod)
    await service._write_file(service.prod_file, prods)
    return new_prod


@router.delete("/{id}")
async def remove_product(id: str, _: UserInfo = Depends(get_current_user)):
    prods = await service._read_file(service.prod_file)
    new_prods = [p for p in prods if p['id'] != id]
    if len(new_prods) == len(prods):
        raise HTTPException(404, "产品不存在")
    await service._write_file(service.prod_file, new_prods)
    return {"message": "产品已删除"}