#!/usr/bin/env python3
"""
文件上传API测试脚本
"""

import requests
import os
from PIL import Image
import io

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

def create_test_image():
    """创建一个测试图片"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (800, 400), color='red')
    
    # 保存到内存
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return img_byte_arr

def test_upload_image(token):
    """测试图片上传"""
    print("测试图片上传...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 创建测试图片
    test_image = create_test_image()
    
    files = {
        'file': ('test_image.jpg', test_image, 'image/jpeg')
    }
    
    response = requests.post(f"{BASE_URL}/api/upload/image", files=files, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 图片上传成功: {result}")
        return result.get("filename")
    else:
        print(f"❌ 图片上传失败: {response.text}")
        return None

def test_get_image(filename):
    """测试获取图片"""
    print(f"\n测试获取图片: {filename}")
    
    response = requests.get(f"{BASE_URL}/api/upload/image/{filename}")
    
    if response.status_code == 200:
        print("✅ 获取图片成功")
        return True
    else:
        print(f"❌ 获取图片失败: {response.text}")
        return False

def test_delete_image(token, filename):
    """测试删除图片"""
    print(f"\n测试删除图片: {filename}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(f"{BASE_URL}/api/upload/image/{filename}", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 删除图片成功: {result}")
        return True
    else:
        print(f"❌ 删除图片失败: {response.text}")
        return False

def test_upload_without_auth():
    """测试未认证上传"""
    print("\n测试未认证上传...")
    
    test_image = create_test_image()
    files = {
        'file': ('test_image.jpg', test_image, 'image/jpeg')
    }
    
    response = requests.post(f"{BASE_URL}/api/upload/image", files=files)
    
    if response.status_code == 401:
        print("✅ 未认证上传被正确拒绝")
        return True
    else:
        print(f"❌ 未认证上传未被拒绝: {response.status_code}")
        return False

def test_invalid_file_type(token):
    """测试无效文件类型"""
    print("\n测试无效文件类型...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 创建一个文本文件
    files = {
        'file': ('test.txt', io.BytesIO(b'This is a text file'), 'text/plain')
    }
    
    response = requests.post(f"{BASE_URL}/api/upload/image", files=files, headers=headers)
    
    if response.status_code == 400:
        result = response.json()
        print(f"✅ 无效文件类型被正确拒绝: {result.get('detail')}")
        return True
    else:
        print(f"❌ 无效文件类型未被拒绝: {response.status_code}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始文件上传API测试...\n")
    
    # 测试未认证上传
    test_upload_without_auth()
    
    # 获取token
    token = get_token()
    if not token:
        print("无法获取token，跳过需要认证的测试")
        return
    
    # 测试无效文件类型
    test_invalid_file_type(token)
    
    # 测试图片上传
    filename = test_upload_image(token)
    
    if filename:
        # 测试获取图片
        test_get_image(filename)
        
        # 测试删除图片
        test_delete_image(token, filename)
    
    print("\n✅ 文件上传API测试完成!")

if __name__ == "__main__":
    main() 