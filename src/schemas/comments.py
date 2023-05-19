from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    comment_text: str = Field(max_length=1500)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    image_id: int
    comment_text: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


