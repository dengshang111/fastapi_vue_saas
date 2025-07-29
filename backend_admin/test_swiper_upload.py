#!/usr/bin/env python3
"""
测试轮播图只能通过文件上传的功能
"""

import requests
import json
import os

# 配置
BASE_URL = "http://localhost:8000"
ACCESS_KEY = "your-access-key-here"  # 请替换为实际的AccessKey

def test_swiper_upload_only():
    """测试轮播图只能通过文件上传"""
    
    headers = {
        "Authorization": f"Bearer {ACCESS_KEY}",
        "Content-Type": "application/json"
    }
    
    print("=== 测试轮播图只能通过文件上传功能 ===\n")
    
    # 1. 获取已上传文件列表
    print("1. 获取已上传文件列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/swiper/uploaded-files", headers=headers)
        if response.status_code == 200:
            files = response.json()
            print(f"   成功获取 {len(files)} 个已上传文件")
            for file in files:
                print(f"   - {file['filename']} ({file['size']} bytes)")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 2. 尝试创建轮播图（不指定文件）
    print("2. 尝试创建轮播图（不指定文件）...")
    try:
        swiper_data = {
            "title": "测试轮播图",
            "filename": "",  # 空文件名
            "sort_order": 1,
            "is_active": True
        }
        response = requests.post(f"{BASE_URL}/api/swiper/", headers=headers, json=swiper_data)
        if response.status_code == 400:
            print("   正确: 返回400错误，不允许空文件名")
        else:
            print(f"   意外: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 3. 尝试创建轮播图（指定不存在的文件）
    print("3. 尝试创建轮播图（指定不存在的文件）...")
    try:
        swiper_data = {
            "title": "测试轮播图",
            "filename": "nonexistent.jpg",  # 不存在的文件
            "sort_order": 1,
            "is_active": True
        }
        response = requests.post(f"{BASE_URL}/api/swiper/", headers=headers, json=swiper_data)
        if response.status_code == 400:
            print("   正确: 返回400错误，文件不存在")
        else:
            print(f"   意外: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 4. 获取轮播图列表
    print("4. 获取轮播图列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/swiper/", headers=headers)
        if response.status_code == 200:
            swipers = response.json()
            print(f"   成功获取 {len(swipers)} 个轮播图")
            for swiper in swipers:
                print(f"   - {swiper['title']}: {swiper['image']}")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 5. 获取公开轮播图列表
    print("5. 获取公开轮播图列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/swiper/public")
        if response.status_code == 200:
            swipers = response.json()
            print(f"   成功获取 {len(swipers)} 个公开轮播图")
            for swiper in swipers:
                print(f"   - {swiper['title']}: {swiper['image']}")
        else:
            print(f"   失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_swiper_upload_only() 