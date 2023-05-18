from typing import List
from fastapi import APIRouter, Depends, Path, status, HTTPException

from src.database.models import User, UserRole
from src.repository import ratings as repository_ratings
from src.schemas.ratings import RatingResponse, AverageRatingResponse
from src.schemas.images import ImageResponse
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/rating', tags=['ratings'])

allowed_operation_get = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_post = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_put = RoleAccess([UserRole.Admin, UserRole.Moderator])
allowed_operation_delete = RoleAccess([UserRole.Admin, UserRole.Moderator])


@router.post("/{image_id}/{rate}", response_model=RatingResponse, dependencies=[Depends(allowed_operation_post)])
async def create_rate(image_id: int, rate: int = Path(description="From one to five stars of rating.", ge=1, le=5),
                      db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_rate function creates a new rate for the image with the given ID. The function takes in an integer
    value from 1 to 5, and returns a JSON object containing information about the newly created rate.

    :param image_id: int: Get the image id from the url
    :param rate: int: Set the rating of an image
    :param ge: Specify the minimum value of the rate
    :param le: Set the maximum value of the rate
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: The new rate
    """
    new_rate = await repository_ratings.create_rate(image_id, rate, db, current_user)
    if new_rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_rate


@router.delete("/delete/{rate_id}", response_model=RatingResponse, dependencies=[Depends(allowed_operation_delete)])
async def delete_rate(rate_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_rate function deletes a rate from the database.
        The function takes in an integer, which is the id of the rate to be deleted.
        It also takes in a Session object and a User object as parameters,
        which are used to access and delete data from the database.

    :param rate_id: int: Get the rate_id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A rate object
    """
    deleted_rate = await repository_ratings.delete_rate(rate_id, db, current_user)
    if deleted_rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rate not found or not available.")
    return deleted_rate


@router.get("/show_image_rating/{image_id}", response_model=AverageRatingResponse)
async def calculate_rating(image_id: int, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The calculate_rating function calculate an average rating of the image.
        The function takes in an integer, which is the id of the image.
        It also takes in a Session object and a User object as parameters,
        which are used to access data from the database.

    :param image_id: int: Get the image_id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: An average rating object
    """
    average_rate = await repository_ratings.calculate_rating(image_id, db, current_user)
    if average_rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found or not available.")
    return { "average_rating": average_rate }


@router.get("/show_images_by_rating", response_model=List[ImageResponse])
async def show_images_by_rating(to_decrease: bool, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The show_images_by_rating function show all images, sorted by rating.
        The function takes a boolean value that indicates the direction of sorting, 
        to increase the rating or to decrease it.
        It also takes in a Session object and a User object as parameters,
        which are used to access data from the database.

    :param to_decrease: bool: Indicates the direction of sorting.
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A list of Images objects, sorted by rating
    """
    images_by_rating = await repository_ratings.show_images_by_rating(to_decrease, db, current_user)
    if images_by_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found or not available.")
    return images_by_rating