from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from src.database.models import User, Comment
from src.schemas.comments import CommentBase


async def create_comment(image_id: int, body: CommentBase, db: Session, user: User) -> Comment:
    """
    Creates a new comment in the database.

    Arguments:
        image_id (int): ID of the image that the comment is being made on
        body (CommentBase): Pass the comment_text from the request body to the function
        db (Session): SQLAlchemy session object for accessing the database
        user (User): the current user attempting to delete the comment

    Returns:
        Comment: the Comment object representing the new comment
    """
    comment = Comment(user_id=user.id,
                      image_id=image_id,
                      created_at=func.now(),
                      comment_text=body.comment_text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def edit_comment(comment_id: int, body: CommentBase, db: Session, user: User) -> Comment | None:
    """
    Modifies the specified comment in the database, if the current user has permission to do so.

    Arguments:
        comment_id (int): ID of the comment to be deleted
        db (Session): SQLAlchemy session object for accessing the database
        body (CommentBase): Pass the comment_text from the request body to the function
        user (User): the current user attempting to edite the comment

    Returns:
        Comment | None: the Comment object representing the modified comment,
        or None if the user have no permission to edite the comment or if no matching comment exists in the database
    """
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user.id)).first()
    if comment:
        comment.comment_text = body.comment_text
        comment.updated_at = func.now()
        db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User) -> Comment | None:
    """
    Deletes the specified comment from the database, if the current user has permission to do so.

    Arguments:
        comment_id (int): ID of the comment to be deleted
        db (Session): SQLAlchemy session object for accessing the database
        user (User): the current user attempting to delete the comment

    Returns:
        Comment | None: the Comment object representing the deleted comment,
        or None if the user have no permission to delete the comment or if no matching comment exists in the database
    """

    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def get_all_user_comments(skip: int, limit: int, user_id: int, db: Session) -> List[Comment] | None:
    """
    Gets all comments from the specified user from the database.

    Arguments:
        skip (int): number of comments to skip in the search
        limit (int): maximum number of comments to retrieve
        user_id (int): ID of the user to retrieve comments for
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        List[Comment] | None: a list of Comment objects representing the user's comments,
        or None if no matching comments were found
    """

    return db.query(Comment).filter(Comment.user_id == user_id).offset(skip).limit(limit).all()


async def get_comments_by_image_id(skip: int, limit: int, image_id: int, db: Session) -> List[Comment] | None:
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
    return db.query(Comment).filter(Comment.image_id == image_id).offset(skip).limit(limit).all()
