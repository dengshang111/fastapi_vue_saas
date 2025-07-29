#!/usr/bin/env python3
"""
测试批量管理和分组功能
"""

import requests
import json
import os
from pathlib import Path

# 配置
BASE_URL = "http://localhost:8000"
TOKEN = "your_access_token_here"  # 请替换为实际的token

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_group_management():
    """测试分组管理功能"""
    print("=== 测试分组管理功能 ===")
    
    # 1. 创建分组
    print("\n1. 创建分组...")
    groups_to_create = ["风景", "人物", "动物", "建筑"]
    
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

def test_file_upload_with_groups():
    """测试带分组的文件上传"""
    print("\n=== 测试带分组的文件上传 ===")
    
    # 创建测试图片
    test_images = [
        ("风景", "landscape.jpg"),
        ("人物", "portrait.jpg"),
        ("动物", "animal.jpg"),
        ("建筑", "building.jpg")
    ]
    
    for group, filename in test_images:
        print(f"\n上传到分组 '{group}': {filename}")
        
        # 创建简单的测试图片文件
        test_file_path = f"test_{filename}"
        with open(test_file_path, "wb") as f:
            f.write(b"fake image data for testing")
        
        try:
            with open(test_file_path, "rb") as f:
                files = {"file": (filename, f, "image/jpeg")}
                data = {"group": group} if group else {}
                
                response = requests.post(
                    f"{BASE_URL}/api/upload/image",
                    headers={"Authorization": f"Bearer {TOKEN}"},
                    files=files,
                    data=data
                )
                
                print(f"  状态码: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"  成功: {result}")
                else:
                    print(f"  失败: {response.text}")
        
        finally:
            # 清理测试文件
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

def test_get_files_by_group():
    """测试按分组获取文件"""
    print("\n=== 测试按分组获取文件 ===")
    
    groups = ["", "风景", "人物", "动物", "建筑"]
    
    for group in groups:
        group_name = group if group else "默认分组"
        print(f"\n获取 {group_name} 的文件...")
        
        url = f"{BASE_URL}/api/upload/files"
        if group:
            url += f"?group={group}"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files = response.json()
            print(f"  文件数量: {len(files)}")
            for file in files[:3]:  # 只显示前3个文件
                print(f"    - {file['filename']} ({file.get('group', '默认分组')})")
        else:
            print(f"  失败: {response.text}")

def test_batch_delete():
    """测试批量删除功能"""
    print("\n=== 测试批量删除功能 ===")
    
    # 1. 获取所有文件
    print("\n1. 获取所有文件...")
    response = requests.get(f"{BASE_URL}/api/upload/files", headers=headers)
    if response.status_code != 200:
        print(f"获取文件列表失败: {response.text}")
        return
    
    all_files = response.json()
    if not all_files:
        print("没有文件可以删除")
        return
    
    # 2. 选择要删除的文件（选择前3个）
    files_to_delete = all_files[:3]
    filenames = [file['filename'] for file in files_to_delete]
    
    print(f"\n2. 准备删除 {len(filenames)} 个文件:")
    for filename in filenames:
        print(f"   - {filename}")
    
    # 3. 执行批量删除
    print(f"\n3. 执行批量删除...")
    response = requests.post(
        f"{BASE_URL}/api/upload/batch-delete",
        headers=headers,
        json={"filenames": filenames}
    )
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"删除成功: {result}")
    else:
        print(f"删除失败: {response.text}")

def test_delete_group():
    """测试删除分组"""
    print("\n=== 测试删除分组 ===")
    
    # 1. 获取分组列表
    response = requests.get(f"{BASE_URL}/api/upload/groups", headers=headers)
    if response.status_code != 200:
        print(f"获取分组列表失败: {response.text}")
        return
    
    groups = response.json()
    if not groups:
        print("没有分组可以删除")
        return
    
    # 2. 删除第一个分组
    group_to_delete = groups[0]['name']
    print(f"\n删除分组: {group_to_delete}")
    
    response = requests.delete(
        f"{BASE_URL}/api/upload/groups/{group_to_delete}",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"删除成功: {result}")
    else:
        print(f"删除失败: {response.text}")

def main():
    """主测试函数"""
    print("开始测试批量管理和分组功能...")
    
    try:
        # 测试分组管理
        test_group_management()
        
        # 测试文件上传
        test_file_upload_with_groups()
        
        # 测试按分组获取文件
        test_get_files_by_group()
        
        # 测试批量删除
        test_batch_delete()
        
        # 测试删除分组
        test_delete_group()
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

if __name__ == "__main__":
    main() 