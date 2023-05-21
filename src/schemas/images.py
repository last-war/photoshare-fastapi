from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from src.schemas.tags import TagResponse


class ImageModel(BaseModel):
    description: str = Field('description min_length 20 simbols', min_length=20, max_length=255)
    tags_text: Optional[str] = Field(None, max_length=25)


class ImageResponse(BaseModel):
    id: int
    image_url: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    description: str
    tags: List[TagResponse]

    class Config:
        orm_mode = True


class ImageTransformationModel(BaseModel):
    id: int
    transformation: str = "standard"
