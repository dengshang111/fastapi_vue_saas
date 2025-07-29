#!/usr/bin/env python3
"""
测试小程序二维码配置功能
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:13286"

def test_qr_code_config():
    """测试小程序二维码配置功能"""
    
    print("=== 测试小程序二维码配置功能 ===\n")
    
    # 1. 测试获取配置
    print("1. 测试获取配置...")
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
    
    # 2. 测试更新配置
    print("2. 测试更新配置...")
    try:
        update_data = {
            "image": "/api/upload/static/test_qr_code.jpg",
            "title": "测试小程序二维码",
            "description": "这是一个测试二维码",
            "enabled": True
        }
        
        response = requests.put(
            f"{BASE_URL}/api/qr-code/config",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("响应:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("错误:", response.text)
    except Exception as e:
        print(f"请求失败: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. 再次获取配置验证更新
    print("3. 验证配置更新...")
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
    
    # 4. 测试公开接口
    print("4. 测试公开接口...")
    try:
        response = requests.get(f"{BASE_URL}/api/qr-code/public")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("响应:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("错误:", response.text)
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_qr_code_config() 