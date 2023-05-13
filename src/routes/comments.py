from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository.comments import create_comment, edit_comment, delete_comment, get_all_user_comments, \
    get_comments_by_image_id
from src.schemas import CommentBase, CommentModel
from src.services.auth import auth_service

router = APIRouter(prefix='/comments', tags=["comments"])


@router.post('/{image_id}', response_model=CommentBase)
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
    :doc-author: Trelent
    """
    comment = await create_comment(image_id, body, db, current_user)

    return comment


@router.put('/{comment_id}', response_model=CommentBase)
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
    :doc-author: Trelent
    """
    updated_comment = await edit_comment(comment_id, body, db, current_user)

    if not updated_comment:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    return updated_comment


@router.delete('/{comment_id}', response_model=CommentModel)
async def remove_comment(comment_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_comment function deletes a comment from the database.

    :param comment_id: int: Specify the id of the comment to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A comment object
    :doc-author: Trelent
    """
    deleted_comment = await delete_comment(comment_id, db, current_user)

    if not deleted_comment:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    return deleted_comment


@router.get('/user/{user_id}', response_model=CommentModel)
async def show_user_comments(user_id: int,
                             db: Session = Depends(get_db)):
    """
    The show_user_comments function returns all comments made by a user.
    Args:
    user_id (int): The id of the user whose comments are to be returned.
    db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).

    :param user_id: int: Specify the user_id of the user whose comments we want to retrieve
    :param db: Session: Pass the database connection to the function
    :return: A list of comments
    :doc-author: Trelent
    """
    comments = await get_all_user_comments(user_id, db)
    return comments


@router.get('/image/{image_id}', response_model=CommentModel)
async def show_comments(image_id: int,
                        db: Session = Depends(get_db)):
    """
    The show_comments function returns a list of comments for the image with the given ID.

    :param image_id: int: Specify the image id
    :param db: Session: Get the database session
    :return: A list of comments
    :doc-author: Trelent
    """
    comments = await get_comments_by_image_id(image_id, db)
    return comments
