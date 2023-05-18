from pydantic import BaseModel, Field


class TagModel(BaseModel):
    tag_name: str = Field(max_length=30)


class TagResponse(TagModel):
    id: int

    class Config:
        orm_mode = True


