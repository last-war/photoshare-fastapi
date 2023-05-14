from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, UserRole
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserResponse, UserModel
from src.services.cloud_image import CloudImage
from src.services.roles import RoleAccess

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service to get the current user.

    :param current_user: User: Get the current user object
    :return: The current user object
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.

    :param file: UploadFile: Receive the file from the client
    :param current_user: User: Get the current user from the database
    :param db: Session: Access the database
    :return: The updated user
    :doc-author: Trelent
    """
    public_id = CloudImage.generate_name_avatar(current_user.email)
    r = CloudImage.upload(file.file, public_id)
    src_url = CloudImage.get_url_for_avatar(public_id, r)
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user


@router.put("/update_user", response_model=UserResponse)
async def update_user(
        body: UserResponse,
        user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    user = await repository_users.update_user(body, user, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return user


@router.put("/update_user_by_admin", response_model=UserResponse)
async def update_user_by_admin(
        body: UserResponse,
        user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    user = await repository_users.update_user_by_admin(body, user, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return user


@router.put("/ban_user", response_model=UserResponse, dependencies=[Depends(RoleAccess([UserRole.Admin]))])
async def ban_user(user_id: int, db: Session = Depends(get_db)):
    ban = await repository_users.ban_user(user_id, db)
    if ban is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return ban
