from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, UserRole
from src.repository.comments import create_comment, edit_comment, delete_comment, get_all_user_comments, \
    get_comments_by_image_id
from src.schemas import CommentBase, CommentModel
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/comments', tags=["comments"])

allowed_operation_get = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_post = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_put = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_delete = RoleAccess([UserRole.Admin])


@router.post('/{image_id}', response_model=CommentBase, dependencies=[Depends(allowed_operation_post)])
async def post_comment(image_id: int,
                       body: CommentBase,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The post_comment function creates a new comment for an image.

    :param image_id: int: Specify the image that the comment is being posted to
    :param body: CommentBase: Get the comment body from the request
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is making the request
    :return: A comment object
    """

    comment = await create_comment(image_id, body, db, current_user)

    return comment


@router.put('/{comment_id}', response_model=CommentBase, dependencies=[Depends(allowed_operation_put)])
async def update_comment(comment_id: int,
                         body: CommentBase,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_comment function updates a comment in the database.

    :param comment_id: int: Specify the comment that is being updated
    :param body: CommentBase: Get the body of the comment
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: The updated comment object
    """

    updated_comment = await edit_comment(comment_id, body, db, current_user)

    if not updated_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return updated_comment


@router.delete('/{comment_id}', response_model=CommentModel, dependencies=[Depends(allowed_operation_delete)])
async def remove_comment(comment_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_comment function deletes a comment from the database.

    :param comment_id: int: Specify the id of the comment to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A comment object
    """

    deleted_comment = await delete_comment(comment_id, db, current_user)

    if not deleted_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return None


@router.get('/user/{user_id}', response_model=CommentModel, dependencies=[Depends(allowed_operation_get)])
async def show_user_comments(user_id: int,
                             db: Session = Depends(get_db),
                             skip: int = 0,
                             limit: int = 10):

    """
    The show_user_comments function returns a list of comments made by the user with the given ID.
    The function takes in an integer representing the user's ID, and two optional parameters: skip and limit.
    Skip is used to specify how many comments should be skipped before returning results, while limit specifies how many results should be returned.

    :param user_id: int: Get the comments of a specific user
    :param db: Session: Pass the database session to the function
    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments to be returned
    :return: A list of comments
    """

    comments = await get_all_user_comments(skip, limit, user_id, db)
    return comments


@router.get('/image/{image_id}', response_model=CommentModel, dependencies=[Depends(allowed_operation_get)])
async def show_comments(image_id: int,
                        db: Session = Depends(get_db),
                        skip: int = 0,
                        limit: int = 10):

    """
    The show_comments function returns a list of comments for the image with the given ID.

    :param image_id: int: Get the image id from the url
    :param db: Session: Get the database session
    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments returned
    :param : Get the image id from the url
    :return: A list of comments for a given image
    """

    comments = await get_comments_by_image_id(skip, limit, image_id, db)
    return comments
