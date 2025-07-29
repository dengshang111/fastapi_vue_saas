from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import json
import os
from datetime import datetime

from auth import get_current_user
from models import UserInfo

router = APIRouter(prefix="/api/product", tags=["产品管理"])

# 数据模型
class Category(BaseModel):
    name: str
    key: str

class CategoryList(BaseModel):
    categories: List[Category]

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    category: str
    description: str = ""
    mainImage: str
    images: List[str] = []

class ProductList(BaseModel):
    products: List[Product]

# 数据文件路径
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "产品")
CATEGORY_FILE = os.path.join(CONFIG_DIR, "categories.json")
PRODUCT_FILE = os.path.join(CONFIG_DIR, "products.json")
UPLOAD_DIR = "uploads"

# 确保数据目录存在
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_categories() -> List[dict]:
    """加载分类数据"""
    if not os.path.exists(CATEGORY_FILE):
        # 初始化默认分类
        default_categories = [{"name": "CY系列", "key": "CY"}]
        save_categories(default_categories)
        return default_categories
    
    try:
        with open(CATEGORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载categories.json失败: {e}")
        return []

def save_categories(categories: List[dict]):
    """保存分类数据"""
    try:
        with open(CATEGORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存categories.json失败: {e}")

def load_products() -> List[dict]:
    """加载产品数据"""
    if not os.path.exists(PRODUCT_FILE):
        save_products([])
        return []
    
    try:
        with open(PRODUCT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载products.json失败: {e}")
        return []

def save_products(products: List[dict]):
    """保存产品数据"""
    try:
        with open(PRODUCT_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存products.json失败: {e}")

def generate_product_id() -> str:
    """生成产品ID"""
    return datetime.now().strftime('%Y%m%d%H%M%S')

# API路由
@router.get("/categories", response_model=CategoryList)
async def get_categories(current_user: UserInfo = Depends(get_current_user)):
    """获取所有分类"""
    try:
        categories: List[dict] = load_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取分类列表失败: {str(e)}"
        )

@router.post("/categories", response_model=Category)
async def create_category(
    category: Category,
    current_user: UserInfo = Depends(get_current_user)
):
    """创建新分类"""
    try:
        categories: List[dict] = load_categories()
        
        # 检查key是否已存在
        if any(c["key"] == category.key for c in categories):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="分类代码已存在"
            )
        
        new_category = category.dict()
        categories.append(new_category)
        save_categories(categories)
        
        return new_category
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建分类失败: {str(e)}"
        )

@router.put("/categories/{key}", response_model=Category)
async def update_category(
    key: str,
    category: Category,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新分类"""
    try:
        categories: List[dict] = load_categories()
        
        # 查找并更新分类
        for i, c in enumerate(categories):
            if c["key"] == key:
                if key != category.key:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="不能修改分类代码"
                    )
                categories[i] = category.dict()
                save_categories(categories)
                return category
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新分类失败: {str(e)}"
        )

@router.delete("/categories/{key}")
async def delete_category(
    key: str,
    current_user: UserInfo = Depends(get_current_user)
):
    """删除分类"""
    try:
        categories: List[dict] = load_categories()
        products = load_products()
        
        # 检查是否有产品使用此分类
        if any(p["category"] == key for p in products):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该分类下还有产品，无法删除"
            )
        
        # 查找并删除分类
        for i, category in enumerate(categories):
            if category["key"] == key:
                categories.pop(i)
                save_categories(categories)
                return {"message": "分类删除成功"}
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除分类失败: {str(e)}"
        )

@router.get("/list", response_model=ProductList)
async def get_products(
    category: Optional[str] = None,
    current_user: UserInfo = Depends(get_current_user)
):
    """获取产品列表"""
    try:
        products = load_products()
        
        if category and category != "all":
            products = [p for p in products if p["category"] == category]
        
        return {"products": products}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取产品列表失败: {str(e)}"
        )

@router.post("/new", response_model=Product)
async def create_product(
    product: Product,
    current_user: UserInfo = Depends(get_current_user)
):
    """创建新产品"""
    try:
        # 验证分类是否存在
        categories = load_categories()
        if not any(c["key"] == product.category for c in categories):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="产品分类不存在"
            )
        
        # 验证图片是否存在
        # 从图片URL中提取路径信息
        # URL格式可能是: /api/upload/static/filename 或 /api/upload/static/group/filename
        main_image_url = product.mainImage
        if main_image_url.startswith("/api/upload/static/"):
            main_image_relative_path = main_image_url[len("/api/upload/static/"):]
        else:
            main_image_relative_path = os.path.basename(main_image_url)
        
        main_image_path = os.path.join(UPLOAD_DIR, main_image_relative_path)
        if not os.path.exists(main_image_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="主图不存在"
            )
        
        for image in product.images:
            # 从图片URL中提取路径信息
            if image.startswith("/api/upload/static/"):
                image_relative_path = image[len("/api/upload/static/"):]
            else:
                image_relative_path = os.path.basename(image)
            
            image_path = os.path.join(UPLOAD_DIR, image_relative_path)
            if not os.path.exists(image_path):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"配色图片不存在: {image}"
                )
        
        products = load_products()
        new_product = product.dict()
        new_product["id"] = generate_product_id()
        products.append(new_product)
        save_products(products)
        
        return new_product
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建产品失败: {str(e)}"
        )

@router.put("/{id}", response_model=Product)
async def update_product(
    id: str,
    product: Product,
    current_user: UserInfo = Depends(get_current_user)
):
    """更新产品"""
    try:
        # 验证分类是否存在
        categories = load_categories()
        if not any(c["key"] == product.category for c in categories):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="产品分类不存在"
            )
        
        # 验证图片是否存在
        # 从图片URL中提取路径信息
        # URL格式可能是: /api/upload/static/filename 或 /api/upload/static/group/filename
        main_image_url = product.mainImage
        if main_image_url.startswith("/api/upload/static/"):
            main_image_relative_path = main_image_url[len("/api/upload/static/"):]
        else:
            main_image_relative_path = os.path.basename(main_image_url)
        
        main_image_path = os.path.join(UPLOAD_DIR, main_image_relative_path)
        if not os.path.exists(main_image_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="主图不存在"
            )
        
        for image in product.images:
            # 从图片URL中提取路径信息
            if image.startswith("/api/upload/static/"):
                image_relative_path = image[len("/api/upload/static/"):]
            else:
                image_relative_path = os.path.basename(image)
            
            image_path = os.path.join(UPLOAD_DIR, image_relative_path)
            if not os.path.exists(image_path):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"配色图片不存在: {image}"
                )
        
        products = load_products()
        
        # 查找并更新产品
        for i, p in enumerate(products):
            if p["id"] == id:
                updated_product = product.dict()
                updated_product["id"] = id
                products[i] = updated_product
                save_products(products)
                return updated_product
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新产品失败: {str(e)}"
        )

@router.delete("/{id}")
async def delete_product(
    id: str,
    current_user: UserInfo = Depends(get_current_user)
):
    """删除产品"""
    try:
        products = load_products()
        
        # 查找并删除产品
        for i, product in enumerate(products):
            if product["id"] == id:
                products.pop(i)
                save_products(products)
                return {"message": "产品删除成功"}
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除产品失败: {str(e)}"
        ) 