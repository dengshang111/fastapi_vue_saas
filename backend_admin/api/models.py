from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class AccessKeyLoginRequest(BaseModel):
    access_key: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

class UserInfo(BaseModel):
    username: str
    is_admin: bool = True

class LogoutResponse(BaseModel):
    message: str 