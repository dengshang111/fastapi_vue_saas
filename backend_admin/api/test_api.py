#!/usr/bin/env python3
"""
API测试脚本
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_login():
    """测试用户名密码登录"""
    print("测试用户名密码登录...")
    
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 登录成功: {result}")
        return result.get("access_token")
    else:
        print(f"❌ 登录失败: {response.text}")
        return None

def test_access_key_login():
    """测试AccessKey登录"""
    print("\n测试AccessKey登录...")
    
    data = {
        "access_key": "admin123456"
    }
    
    response = requests.post(f"{BASE_URL}/api/login/access-key", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ AccessKey登录成功: {result}")
        return result.get("access_token")
    else:
        print(f"❌ AccessKey登录失败: {response.text}")
        return None

def test_user_info(token):
    """测试获取用户信息"""
    print("\n测试获取用户信息...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/api/user/info", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 获取用户信息成功: {result}")
    else:
        print(f"❌ 获取用户信息失败: {response.text}")

def test_dashboard(token):
    """测试获取仪表板数据"""
    print("\n测试获取仪表板数据...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/api/dashboard", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 获取仪表板数据成功: {result}")
    else:
        print(f"❌ 获取仪表板数据失败: {response.text}")

def test_logout(token):
    """测试退出登录"""
    print("\n测试退出登录...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(f"{BASE_URL}/api/logout", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 退出登录成功: {result}")
    else:
        print(f"❌ 退出登录失败: {response.text}")

def main():
    """主测试函数"""
    print("🚀 开始API测试...\n")
    
    # 测试用户名密码登录
    token1 = test_login()
    
    if token1:
        # 测试获取用户信息
        test_user_info(token1)
        
        # 测试获取仪表板数据
        test_dashboard(token1)
        
        # 测试退出登录
        test_logout(token1)
    
    # 测试AccessKey登录
    token2 = test_access_key_login()
    
    if token2:
        # 测试获取用户信息
        test_user_info(token2)
        
        # 测试获取仪表板数据
        test_dashboard(token2)
        
        # 测试退出登录
        test_logout(token2)
    
    print("\n✅ API测试完成!")

if __name__ == "__main__":
    main() 