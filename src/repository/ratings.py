from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from starlette import status

from src.database.models import Rating, User, Image


async def create_rate(image_id: int, rate: int, db: Session, user: User) -> Rating:
    """
    The create_rate function creates a new rate for the image with the given id.

    Args:
        image_id (int): The id of the image to be rated.
        rate (int): The rating value.
        db (Session): SQLAlchemy session object for accessing the database
        user (User): The User object that is creating the rate.

    Returns:
        Comment: the Rating object representing the new rating.
    """
    is_self_image = db.query(Image).filter(Image.id == image_id).first().user_id == user.id
    already_rated = db.query(Rating).filter(and_(Rating.image_id == image_id, Rating.user_id == user.id)).first()
    image_exists = db.query(Image).filter(Image.id == image_id).first()
    if is_self_image:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="It`s not possible to rate own image.")
    if already_rated:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="It`s not possible to rate twice.")
    if image_exists:
        new_rate = Rating(image_id=image_id, rate=rate, user_id=user.id)
        db.add(new_rate)
        db.commit()
        db.refresh(new_rate)
        return new_rate
    

async def delete_rate(rate_id: int, db: Session, user: User) -> None:
    """
    The delete_rate function deletes a rating from the database.

    Args:
        rate_id (int): The id of the rating to be deleted.
        db (Session): A connection to the database.
        user (User): The User object that is removes the rate.

    Returns:
        None
    """
    rate = db.query(Rating).filter(Rating.id == rate_id).first()
    if rate:
        db.delete(rate)
        db.commit()
    return None


async def calculate_rating(image_id: int, db: Session, user: User) -> float | None:
    """
    The calculate_rating function calculate an average rating of the image.

    Args:
        image_id (int): The id of the image for calculating rating.
        db (Session): A connection to the database.
        user (User): The User object which calculates the rating.

    Returns:
        float: The average rating of the image
    """
    rating = db.query(func.avg(Rating.rate)).filter(Rating.image_id == image_id).scalar()
    return rating
    

async def show_images_by_rating(to_decrease: bool, db: Session, user: User) -> List[Image] | list:
    """
    The show_images_by_rating function show all images in db, sorted by rating.

    Args:
        to_decrease (bool): The boolean value, that indicates the direction of sorting.
        db (Session): A connection to the database.
        user (User): The User object which asks for a list of sorted images

    Returns:
        List[Image] | None: a list of Image objects sorted by rating
        or list if no matching rate
    """
    if to_decrease:
        images = db.query(Image, func.avg(Rating.rate).label('rate')).join(Rating).order_by(desc('rate')).group_by(Image).all()
    else:
        images = db.query(Image, func.avg(Rating.rate).label('rate')).join(Rating).order_by('rate').group_by(Image).all()
    rez = []
    for image in images:
        rez.append(image.Image)
    return rez
