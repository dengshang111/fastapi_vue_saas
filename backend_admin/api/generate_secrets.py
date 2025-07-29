import secrets
import uuid
import base64

def generate_secret_key(length=32):
    """生成一个安全的随机密钥"""
    return base64.b64encode(secrets.token_bytes(length)).decode('utf-8')

def generate_uuid():
    """生成一个UUID"""
    return str(uuid.uuid4())

if __name__ == "__main__":
    # 生成密钥
    secret_key = generate_secret_key()
    # 生成UUID
    uuid_str = generate_uuid()
    
    print("生成的配置信息如下：")
    print(f"SECRET_KEY={secret_key}")
    print(f"ALGORITHM=HS256")
    print(f"UUID={uuid_str}")
    
    print("\n你可以将这些信息复制到你的配置文件中。")
    print("注意：请妥善保管SECRET_KEY，不要泄露给他人。") 