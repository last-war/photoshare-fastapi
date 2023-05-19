from pydantic import BaseModel, Field


class TagModel(BaseModel):
    tag_name: str = Field(max_length=30)


class TagResponse(BaseModel):
    id: int
    tag_name: str

    class Config:
        orm_mode = True


