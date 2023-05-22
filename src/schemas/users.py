from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    login: str = Field(min_length=4, max_length=12)
    email: str = Field(min_length=4, max_length=120)
    password_checksum: str = Field(min_length=6)


class UserResponse(BaseModel):
    id: int
    login: str
    email: str
    role: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_pic_url: Optional[str]
    name: Optional[str]
    is_active: bool
    password_checksum: str
    refresh_token: Optional[str]

    class Config:
        orm_mode = True


class UserChangeRole(BaseModel):
    id: int
    role: int
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    email: str
    updated_at: Optional[datetime]
    user_pic_url: Optional[str]
    name: Optional[str]
    password_checksum: str

    class Config:
        orm_mode = True


class UserUpdateAdmin(BaseModel):
    id: int
    login: str
    email: str
    role: int
    updated_at: Optional[datetime]
    user_pic_url: Optional[str]
    name: Optional[str]
    is_active: bool
    password_checksum: str

    class Config:
        orm_mode = True


class UserShow(BaseModel):
    id: int
    login: str
    email: str
    role: int
    user_pic_url: Optional[str]
    name: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True


class UserDb(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
