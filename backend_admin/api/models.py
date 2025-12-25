from pydantic import BaseModel
from typing import Optional
from tortoise.models import Model
from tortoise import fields
from datetime import datetime

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


class TimestampMixin:
    """时间戳混入类"""
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class User(TimestampMixin, Model):
    """用户模型"""
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password_hash = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username
