from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from starlette import status

from src.database.models import Rating, User, Image


async def create_rate(image_id: int, rate: int, db: Session, user: User) -> Rating:
    """
    The create_rate function creates a new rate for the image with the given id.
        Args:
            image_id (int): The id of the image to be rated.
            rate (int): The rating value.
            user (User): The User object that is creating the rate.

    :param image_id: int: Get the image id from the request
    :param rate: int: Set the rate of the image
    :param db: Session: Access the database
    :param user: User: Get the user_id of the logged in user
    :return: A rating object
    """
    is_self_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()
    already_rated = db.query(Rating).filter(and_(Rating.image_id == image_id, Rating.user_id == user.id)).first()
    image_exists = db.query(Image).filter(Image.id == image_id).first()
    if is_self_image:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="It`s not possible to rate own image.")
    elif already_rated:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="It`s not possible to rate twice.")
    elif image_exists:
        new_rate = Rating(
            image_id=image_id,
            rate=rate,
            user_id=user.id
        )
        db.add(new_rate)
        db.commit()
        db.refresh(new_rate)
        return new_rate
    

async def delete_rate(rate_id: int, db: Session, user: User) -> Rating | None:
    """
    The delete_rate function deletes a rating from the database.
        Args:
            rate_id (int): The id of the rating to be deleted.
            db (Session): A connection to the database.
            user (User): The User object that is removes the rate.

    :param rate_id: int: Specify the id of the rate to be deleted
    :param db: Session: Access the database
    :param user: User: Check if the user is logged in
    :return: The deleted rate
    """
    rate = db.query(Rating).filter(Rating.id == rate_id).first()
    if rate:
        db.delete(rate)
        db.commit()
    return rate

async def calculate_rating(image_id: int, db: Session, user: User) -> float | None:
    """
    The calculate_rating function calculate an average rating of the image.
        Args:
            image_id (int): The id of the image for calculating rating.
            db (Session): A connection to the database.
            user (User): The User object which calculates the rating.

    :param image_id: int: Specify the id of the image for calculating
    :param db: Session: Access the database
    :param user: User: Check if the user is logged in
    :return: The average rating of the image
    """
    image_ratings = db.query(Rating).filter(Rating.image_id == image_id).all()
    if image_ratings:
        rates = [rate.rate for rate in image_ratings]
        rating = round(sum(rates) / len(rates), 2)
        return rating
    

async def show_images_by_rating(to_decrease: bool, db: Session, user: User) -> List[Image] | None:
    """
    The show_images_by_rating function show all images in db, sorted by rating.
        Args:
            to_decrease (bool): The boolean value, that indicates the direction of sorting.
            db (Session): A connection to the database.
            user (User): The User object which asks for a list of sorted images
    """
    images = db.query(Image).all()
    if images:
        images_with_rating = []
        for image in images:
            image_ratings = db.query(Rating).filter(Rating.image_id == image.id).all()

            if image_ratings:
                rates = [rate.rate for rate in image_ratings]
                rating = round(sum(rates) / len(rates), 2)
            else:
                rating = 0
            images_with_rating.append({ "rating": rating,
                                        "image" : image})
        images_with_rating.sort(key=lambda x: x["rating"], reverse=to_decrease)
        return [image["image"] for image in images_with_rating]