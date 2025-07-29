#!/usr/bin/env python3
"""
测试导入是否正常
"""

def test_imports():
    """测试所有模块的导入"""
    try:
        print("测试导入 auth 模块...")
        from auth import get_current_user, create_access_token, verify_token
        print("✅ auth 模块导入成功")
        
        print("测试导入 models 模块...")
        from models import UserInfo, LoginRequest
        print("✅ models 模块导入成功")
        
        print("测试导入 config 模块...")
        from config import settings
        print("✅ config 模块导入成功")
        
        print("测试导入 routers.swiper 模块...")
        from routers import swiper
        print("✅ routers.swiper 模块导入成功")
        
        print("测试导入 routers.upload 模块...")
        from routers import upload
        print("✅ routers.upload 模块导入成功")
        
        print("测试导入 main 模块...")
        from main import app
        print("✅ main 模块导入成功")
        
        print("\n🎉 所有模块导入测试通过！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    test_imports() 