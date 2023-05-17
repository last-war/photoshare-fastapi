from fastapi import APIRouter, Depends, Path, status, HTTPException

from src.database.models import User, UserRole
from src.repository import ratings as repository_ratings
from src.schemas.schemas import RatingResponse
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


@router.delete("/delete/{rate_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_delete)])
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
    return None
