from sqlalchemy.orm import Session

from src.database.models import User, Image
from src.schemas import ImageModel
from fastapi import File


"""
Asynchronous functions for interaction with the database with the images table.
"""


async def create(body: ImageModel, file: File, user: User, db: Session):
    image = Image(**body.dict(), user=user)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image
