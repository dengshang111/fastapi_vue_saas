#!/usr/bin/env python3
"""
配置测试脚本
用于验证新的配置逻辑是否正常工作
"""

import os
from configs.config import settings

def test_config():
    """测试配置加载"""
    print("=== 配置测试 ===")
    print(f"应用名称: {settings.app_name}")
    print(f"调试模式: {settings.debug}")
    print(f"密钥算法: {settings.algorithm}")
    print(f"Token过期时间: {settings.access_token_expire_minutes} 分钟")
    print(f"管理员用户名: {settings.admin_username}")
    print(f"允许的域名: {settings.allowed_origins}")
    print(f"域名类型: {type(settings.allowed_origins)}")
    
    # 测试环境变量覆盖
    print("\n=== 环境变量测试 ===")
    test_env_vars = {
        "APP_NAME": "测试应用",
        "DEBUG": "false",
        "ALLOWED_ORIGINS": "http://localhost:3000,http://localhost:8080"
    }
    
    for key, value in test_env_vars.items():
        print(f"设置环境变量 {key}={value}")
        os.environ[key] = value
    
    # 重新创建设置实例
    from configs.config import Settings
    test_settings = Settings()
    
    print(f"覆盖后的应用名称: {test_settings.app_name}")
    print(f"覆盖后的调试模式: {test_settings.debug}")
    print(f"覆盖后的允许域名: {test_settings.allowed_origins}")
    
    # 清理环境变量
    for key in test_env_vars:
        if key in os.environ:
            del os.environ[key]

if __name__ == "__main__":
    test_config() 