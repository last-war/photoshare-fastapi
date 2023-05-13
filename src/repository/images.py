from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import User, Image
from src.schemas import ImageModel
from fastapi import File


"""
Asynchronous functions for interaction with the database with the images table.
"""


async def create(body: ImageModel, image_url: str, user: User, db: Session):
    image = Image(**body.dict(), user=user, image_url=image_url)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_image_from_id(image_id: int, user: User, db: Session):
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user.id == user.id)).first()
    return image


async def remove(image_id: int, user: User, db: Session):
    image = get_image_from_id(image_id, user, db)
    if image:
        image.is_deleted = True
        db.commit()
    return image
