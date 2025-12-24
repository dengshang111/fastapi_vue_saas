from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import Field
import os

class Settings(BaseSettings):
    # 应用配置
    app_name: str = Field(default="后台管理系统", alias="APP_NAME")
    debug: bool = Field(default=True, alias="DEBUG")
    
    # 安全配置
    secret_key: str = Field(default="your-secret-key-here-change-in-production", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: float = Field(default=1.0, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # AccessKey配置
    admin_access_key: str = Field(default="admin123456", alias="ADMIN_ACCESS_KEY")
    admin_username: str = Field(default="admin", alias="ADMIN_USERNAME")
    admin_password: str = Field(default="admin123", alias="ADMIN_PASSWORD")
    
    # CORS配置
    allowed_origins: List[str] = Field(default=["*"], alias="ALLOWED_ORIGINS")
    
    class Config:
        env_file = ".env"
        # 使用别名来映射环境变量
        populate_by_name = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 处理 ALLOWED_ORIGINS 字符串解析
        if isinstance(self.allowed_origins, str):
            # 如果是字符串，尝试解析为列表
            if self.allowed_origins.strip() == "*":
                self.allowed_origins = ["*"]
            else:
                # 简单的字符串分割，移除空格和引号
                origins = self.allowed_origins.replace('"', '').replace("'", "")
                self.allowed_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]
        
    def print_config(self):
        """打印所有配置属性及其值"""
        print("\n=== 当前配置信息 ===")
        print(f"应用名称: {self.app_name}")
        print(f"调试模式: {self.debug}")
        print(f"密钥: {self.secret_key}")
        print(f"加密算法: {self.algorithm}")
        print(f"Token过期时间: {self.access_token_expire_minutes}分钟")
        print(f"管理员访问密钥: {self.admin_access_key}")
        print(f"管理员用户名: {self.admin_username}")
        print(f"管理员密码: {self.admin_password}")
        print(f"允许的源: {self.allowed_origins}")
        print("==================\n")

# 创建全局设置实例
settings = Settings()


# 为了向后兼容，保留 ALLOWED_ORIGINS 变量
ALLOWED_ORIGINS = settings.allowed_origins 