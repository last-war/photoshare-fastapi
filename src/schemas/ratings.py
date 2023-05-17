from pydantic import BaseModel


class AverageRatingResponse(BaseModel):
    average_rating: float


class RatingModel(BaseModel):
    rate: int


class RatingResponse(RatingModel):
    id: int
    user_id: int
    image_id: int

    class Config:
        orm_mode = True


