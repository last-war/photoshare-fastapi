from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, BaseConfig


class UserModel(BaseModel):
    pass


class UserDb(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    status: str = 'User added'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

      
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
    tags: str = Field('tags', min_length=5, max_length=25)

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class ImageResponse(ImageModel):
    id: int
    image_url: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RatingModel(BaseModel):
    pass


class RatingResponse(RatingModel):
    id: int

    class Config:
        orm_mode = True


class TagModel(BaseModel):
    pass


class TagResponse(TagModel):
    id: int

    class Config:
        orm_mode = True


class RequestEmail(BaseModel):
    email: EmailStr
