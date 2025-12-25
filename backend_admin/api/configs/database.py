from tortoise import Tortoise
from fastapi import FastAPI
import os
from contextlib import asynccontextmanager

# 1. 优化配置读取：增加默认值与类型转换
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "fastapi_vue_saas")
# 建议在模型中直接引用具体的模块路径，如 "api.models" 而非 "models" 以防导入失败
MODELS_LIST = ["models"]

TORTOISE_ORM = {
    "connections": {
        "default": f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
    },
    "apps": {
        "models": {
            "models": MODELS_LIST,
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}


# 2. 推荐使用 lifespan 替代 init_db 函数（FastAPI 官方推荐模式）
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：初始化连接
    await Tortoise.init(config=TORTOISE_ORM)
    # 自动生成表（建议生产环境关闭，改用 aerich 迁移）
    if os.getenv("ENV") == "dev":
        await Tortoise.generate_schemas()

    yield

    # 关闭时：释放连接
    await Tortoise.close_connections()


# 3. 如果你依然想手动调用 init_db，请确保注册方式正确
async def init_db(app: FastAPI):
    """
    初始化数据库连接的替代方案
    注意：Tortoise 官方也提供了 register_tortoise 简化注册
    """
    await Tortoise.init(config=TORTOISE_ORM)
    if os.getenv("DEBUG") == "True":
        await Tortoise.generate_schemas()