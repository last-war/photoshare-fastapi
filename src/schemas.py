from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


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


class ImageModel(BaseModel):
    pass


class ImageResponse(ImageModel):
    id: int

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

