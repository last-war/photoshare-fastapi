from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, BaseConfig


class UserModel(BaseModel):
    login: str = Field(min_length=4, max_length=12)
    email: EmailStr
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

      
class CommentBase(BaseModel):
    comment_text: str = Field(max_length=1500)


class CommentModel(CommentBase):
    id: int
    user_id: int
    image_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
     

class ImageModel(BaseModel):
    description: str = Field('description', min_length=20, max_length=255)
    # TODO tags:

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class ImageResponse(ImageModel):
    id: int
    image_url: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ImageTransformationModel(BaseModel):
    id: int
    transformation: str


class RatingModel(BaseModel):
    rate: int


class RatingResponse(RatingModel):
    id: int
    user_id: int
    image_id: int

    class Config:
        orm_mode = True


class TagModel(BaseModel):
    tag_name: str = Field(max_length=30)


class TagResponse(TagModel):
    id: int
    tag_name: str

    class Config:
        orm_mode = True


class RequestEmail(BaseModel):
    email: EmailStr
