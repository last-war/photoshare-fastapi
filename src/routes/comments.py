from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, UserRole
from src.repository.comments import create_comment, edit_comment, delete_comment, get_all_user_comments, \
    get_comments_by_image_id
from src.schemas.comments import CommentBase, CommentResponse
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/comments', tags=["comments"])

allowed_operation_get = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_post = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_put = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_delete = RoleAccess([UserRole.Admin])


@router.post('/{image_id}', response_model=CommentResponse, dependencies=[Depends(allowed_operation_post)])
async def post_comment(image_id: int,
                       body: CommentBase,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Creates a new comment for an image.

    Arguments:
        image_id (int): ID of the image that the comment is being made on
        body (CommentBase): Pass the comment_text from the request body to the function
        db (Session): SQLAlchemy session object for accessing the database
        current_user (User): the current user attempting to delete the comment

    Returns:
        Comment: the Comment object
    """

    comment = await create_comment(image_id, body, db, current_user)

    return comment


@router.put('/{comment_id}', response_model=CommentResponse, dependencies=[Depends(allowed_operation_put)])
async def update_comment(comment_id: int,
                         body: CommentBase,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):

    """
    Modifies the specified comment in the database, if the current user has permission to do so.
    If comment with requested id does not exist raise HTTPException with status HTTP_404_NOT_FOUND

    Arguments:
        comment_id (int): ID of the comment to be deleted
        db (Session): SQLAlchemy session object for accessing the database
        body (CommentBase): Pass the comment_text from the request body to the function
        current_user (User): the current user attempting to edite the comment

    Returns:
        Comment: the Comment object representing the modified comment,
    """

    updated_comment = await edit_comment(comment_id, body, db, current_user)

    if not updated_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return updated_comment


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_delete)])
async def remove_comment(comment_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Deletes the specified comment from the database, if the current user has permission to do so.
    If comment with requested id does not exist raise HTTPException with status HTTP_404_NOT_FOUND

    Arguments:
        comment_id (int): ID of the comment to be deleted
        db (Session): SQLAlchemy session object for accessing the database
        current_user (User): the current user attempting to delete the comment

    Returns:
        None: If comment was success delete
        """

    deleted_comment = await delete_comment(comment_id, db, current_user)

    if not deleted_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return None


@router.get('/user/{user_id}', response_model=List[CommentResponse], dependencies=[Depends(allowed_operation_get)])
async def show_user_comments(user_id: int,
                             db: Session = Depends(get_db),
                             skip: int = 0,
                             limit: int = 10):

    """
    Gets a list of comments made by the specified user.

    Arguments:
        skip (int): number of comments to skip in the search
        limit (int): maximum number of comments to retrieve
        user_id (int): ID of the user to retrieve comments for
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        List[Comment] | None: a list of Comment objects representing the user's comments,
        or None if no matching comments were found
    """
    comments = await get_all_user_comments(skip, limit, user_id, db)
    return comments


@router.get('/image/{image_id}', response_model=List[CommentResponse], dependencies=[Depends(allowed_operation_get)])
async def show_comments(image_id: int,
                        db: Session = Depends(get_db),
                        skip: int = 0,
                        limit: int = 10):

    """
    Gets all comments of the specified image from the database.

    Arguments:
        skip (int): number of comments to skip in the search
        limit (int): maximum number of comments to retrieve
        image_id (int): ID of the image to retrieve comments for
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        List[Comment] | None: a list of Comment objects representing all comments,
        or None if no matching comments were found
    """
    comments = await get_comments_by_image_id(skip, limit, image_id, db)
    return comments
