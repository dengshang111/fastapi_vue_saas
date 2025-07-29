#!/usr/bin/env python3
"""
测试新添加的分组管理和批量操作接口
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
TOKEN = "admin123456"  # 使用AccessKey登录

def get_token():
    """获取访问令牌"""
    response = requests.post(f"{BASE_URL}/api/login/access-key", json={"access_key": TOKEN})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"登录失败: {response.text}")
        return None

def test_groups_api():
    """测试分组管理接口"""
    print("=== 测试分组管理接口 ===")
    
    token = get_token()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 1. 创建分组
    print("\n1. 创建分组...")
    groups_to_create = ["风景", "人物", "动物"]
    
    for group_name in groups_to_create:
        response = requests.post(
            f"{BASE_URL}/api/upload/groups",
            headers=headers,
            json={"name": group_name}
        )
        print(f"创建分组 '{group_name}': {response.status_code}")
        if response.status_code == 200:
            print(f"  - 成功: {response.json()}")
        else:
            print(f"  - 失败: {response.text}")
    
    # 2. 获取分组列表
    print("\n2. 获取分组列表...")
    response = requests.get(f"{BASE_URL}/api/upload/groups", headers=headers)
    if response.status_code == 200:
        groups = response.json()
        print(f"分组列表: {json.dumps(groups, indent=2, ensure_ascii=False)}")
    else:
        print(f"获取分组列表失败: {response.text}")

def test_files_api():
    """测试文件列表接口"""
    print("\n=== 测试文件列表接口 ===")
    
    token = get_token()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 1. 获取默认分组的文件
    print("\n1. 获取默认分组的文件...")
    response = requests.get(f"{BASE_URL}/api/upload/files", headers=headers)
    if response.status_code == 200:
        files = response.json()
        print(f"默认分组文件数量: {len(files)}")
        for file in files[:3]:  # 只显示前3个
            print(f"  - {file['filename']}")
    else:
        print(f"获取文件列表失败: {response.text}")
    
    # 2. 获取指定分组的文件
    print("\n2. 获取指定分组的文件...")
    response = requests.get(f"{BASE_URL}/api/upload/files?group=风景", headers=headers)
    if response.status_code == 200:
        files = response.json()
        print(f"风景分组文件数量: {len(files)}")
        for file in files[:3]:  # 只显示前3个
            print(f"  - {file['filename']}")
    else:
        print(f"获取分组文件列表失败: {response.text}")

def main():
    """主测试函数"""
    print("开始测试新添加的API接口...")
    
    try:
        test_groups_api()
        test_files_api()
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    main() 