#!/usr/bin/env python3
"""
测试用户管理页面的图片上传、预览和删除功能
"""

import requests
import json
import os

# 配置
BASE_URL = "http://localhost:8000"
ACCESS_KEY = "your-access-key-here"  # 请替换为实际的AccessKey

def test_user_manage_features():
    """测试用户管理功能"""
    
    headers = {
        "Authorization": f"Bearer {ACCESS_KEY}",
        "Content-Type": "application/json"
    }
    
    print("=== 测试用户管理页面功能 ===\n")
    
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
    
    # 2. 测试图片预览功能
    print("2. 测试图片预览功能...")
    try:
        # 先获取文件列表
        response = requests.get(f"{BASE_URL}/api/swiper/uploaded-files", headers=headers)
        if response.status_code == 200:
            files = response.json()
            if files:
                # 测试第一个文件的预览
                test_file = files[0]
                preview_url = f"{BASE_URL}{test_file['url']}"
                print(f"   测试预览文件: {test_file['filename']}")
                print(f"   预览URL: {preview_url}")
                
                # 测试图片访问
                img_response = requests.get(preview_url)
                if img_response.status_code == 200:
                    print("   ✓ 图片预览功能正常")
                else:
                    print(f"   ✗ 图片预览失败: {img_response.status_code}")
            else:
                print("   没有文件可测试预览")
        else:
            print(f"   获取文件列表失败: {response.status_code}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 3. 测试文件删除功能（注意：这会真正删除文件）
    print("3. 测试文件删除功能...")
    print("   注意：此测试会真正删除文件，请确认是否继续？")
    print("   输入 'yes' 继续测试，其他任意键跳过...")
    
    user_input = input().strip().lower()
    if user_input == 'yes':
        try:
            # 先获取文件列表
            response = requests.get(f"{BASE_URL}/api/swiper/uploaded-files", headers=headers)
            if response.status_code == 200:
                files = response.json()
                if files:
                    # 选择最后一个文件进行删除测试
                    test_file = files[-1]
                    print(f"   测试删除文件: {test_file['filename']}")
                    
                    delete_response = requests.delete(
                        f"{BASE_URL}/api/upload/image/{test_file['filename']}", 
                        headers=headers
                    )
                    
                    if delete_response.status_code == 200:
                        print("   ✓ 文件删除成功")
                        
                        # 验证文件是否真的被删除
                        verify_response = requests.get(f"{BASE_URL}/api/swiper/uploaded-files", headers=headers)
                        if verify_response.status_code == 200:
                            remaining_files = verify_response.json()
                            if len(remaining_files) == len(files) - 1:
                                print("   ✓ 文件删除验证成功")
                            else:
                                print("   ✗ 文件删除验证失败")
                    else:
                        print(f"   ✗ 文件删除失败: {delete_response.status_code}")
                else:
                    print("   没有文件可测试删除")
            else:
                print(f"   获取文件列表失败: {response.status_code}")
        except Exception as e:
            print(f"   错误: {e}")
    else:
        print("   跳过删除测试")
    
    print()
    
    # 4. 测试轮播图管理（验证只能通过文件上传）
    print("4. 测试轮播图管理（验证只能通过文件上传）...")
    try:
        # 尝试创建轮播图（不指定文件）
        swiper_data = {
            "title": "测试轮播图",
            "filename": "",  # 空文件名
            "sort_order": 1,
            "is_active": True
        }
        response = requests.post(f"{BASE_URL}/api/swiper/", headers=headers, json=swiper_data)
        if response.status_code == 400:
            print("   ✓ 正确拒绝空文件名的轮播图创建")
        else:
            print(f"   ✗ 意外接受空文件名: {response.status_code}")
            
        # 尝试创建轮播图（指定不存在的文件）
        swiper_data = {
            "title": "测试轮播图",
            "filename": "nonexistent.jpg",  # 不存在的文件
            "sort_order": 1,
            "is_active": True
        }
        response = requests.post(f"{BASE_URL}/api/swiper/", headers=headers, json=swiper_data)
        if response.status_code == 400:
            print("   ✓ 正确拒绝不存在文件的轮播图创建")
        else:
            print(f"   ✗ 意外接受不存在文件: {response.status_code}")
            
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_user_manage_features() 