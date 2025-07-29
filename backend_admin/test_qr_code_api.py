#!/usr/bin/env python3
"""
测试小程序二维码API
"""

import requests
import json
import os

# API基础URL
BASE_URL = "http://localhost:13286"

def test_qr_code_api():
    """测试小程序二维码API"""
    
    # 1. 测试获取配置（需要认证）
    print("=== 测试获取小程序二维码配置 ===")
    try:
        response = requests.get(f"{BASE_URL}/api/qr-code/config")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("响应:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("错误:", response.text)
    except Exception as e:
        print(f"请求失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. 测试公开接口（无需认证）
    print("=== 测试公开小程序二维码配置 ===")
    try:
        response = requests.get(f"{BASE_URL}/api/qr-code/public")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("响应:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("错误:", response.text)
    except Exception as e:
        print(f"请求失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. 检查配置文件
    print("=== 检查配置文件 ===")
    config_file = "api/config/小程序二维码/config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print("配置文件内容:")
            print(json.dumps(config, indent=2, ensure_ascii=False))
    else:
        print("配置文件不存在")
    
    print("\n" + "="*50 + "\n")
    
    # 4. 测试根路径
    print("=== 测试API根路径 ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("响应:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("错误:", response.text)
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_qr_code_api() 