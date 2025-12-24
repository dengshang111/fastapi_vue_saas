#!/usr/bin/env python3
"""
轮播图API测试脚本
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def get_token():
    """获取认证token"""
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("access_token")
    else:
        print("登录失败，无法获取token")
        return None

def test_public_swiper():
    """测试公开轮播图接口"""
    print("测试公开轮播图接口...")
    
    response = requests.get(f"{BASE_URL}/api/swiper/public")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 获取公开轮播图成功: {len(result)} 张图片")
        for item in result:
            print(f"  - {item['title']}: {item['image']}")
        return result
    else:
        print(f"❌ 获取公开轮播图失败: {response.text}")
        return []

def test_admin_swiper_list(token):
    """测试管理员轮播图列表接口"""
    print("\n测试管理员轮播图列表接口...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/api/swiper/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 获取管理员轮播图列表成功: {len(result)} 张图片")
        return result
    else:
        print(f"❌ 获取管理员轮播图列表失败: {response.text}")
        return []

def test_create_swiper(token):
    """测试创建轮播图"""
    print("\n测试创建轮播图...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": "测试轮播图",
        "image": "https://via.placeholder.com/800x400/FF6B6B/FFFFFF?text=Test+Swiper",
        "sort_order": 999,
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/api/swiper/", json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 创建轮播图成功: {result}")
        return result.get("id")
    else:
        print(f"❌ 创建轮播图失败: {response.text}")
        return None

def test_update_swiper(token, swiper_id):
    """测试更新轮播图"""
    print(f"\n测试更新轮播图 (ID: {swiper_id})...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": "更新后的测试轮播图",
        "sort_order": 888
    }
    
    response = requests.put(f"{BASE_URL}/api/swiper/{swiper_id}", json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 更新轮播图成功: {result}")
    else:
        print(f"❌ 更新轮播图失败: {response.text}")

def test_toggle_swiper_status(token, swiper_id):
    """测试切换轮播图状态"""
    print(f"\n测试切换轮播图状态 (ID: {swiper_id})...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(f"{BASE_URL}/api/swiper/{swiper_id}/toggle", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 切换轮播图状态成功: {result}")
    else:
        print(f"❌ 切换轮播图状态失败: {response.text}")

def test_delete_swiper(token, swiper_id):
    """测试删除轮播图"""
    print(f"\n测试删除轮播图 (ID: {swiper_id})...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(f"{BASE_URL}/api/swiper/{swiper_id}", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 删除轮播图成功: {result}")
    else:
        print(f"❌ 删除轮播图失败: {response.text}")

def main():
    """主测试函数"""
    print("🚀 开始轮播图API测试...\n")
    
    # 测试公开接口
    test_public_swiper()
    
    # 获取token
    token = get_token()
    if not token:
        print("无法获取token，跳过需要认证的测试")
        return
    
    # 测试管理员接口
    test_admin_swiper_list(token)
    
    # 测试创建轮播图
    new_swiper_id = test_create_swiper(token)
    
    if new_swiper_id:
        # 测试更新轮播图
        test_update_swiper(token, new_swiper_id)
        
        # 测试切换状态
        test_toggle_swiper_status(token, new_swiper_id)
        
        # 测试删除轮播图
        test_delete_swiper(token, new_swiper_id)
    
    print("\n✅ 轮播图API测试完成!")

if __name__ == "__main__":
    main() 