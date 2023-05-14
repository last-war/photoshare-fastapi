from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.models import User, Comment, UserRole
from src.schemas import CommentBase


async def create_comment(image_id: int, body: CommentBase, db: Session, user: User) -> Comment:
    """
    The create_comment function creates a new comment in the database.

    :param image_id: int: Specify the image that the comment is being made on
    :param body: CommentBase: Pass the comment_text from the request body to the function
    :param db: Session: Access the database
    :param user: User: Get the user id from the token
    :return: A comment object
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
    The edit_comment function takes in a comment_id, body, db and user.
    It then queries the database for the comment with that id. If it exists,
    it checks if the user is an admin or moderator or if they are the owner of
    that particular comment. If so, it updates their text and updated_at time to now.

    :param comment_id: int: Find the comment in the database
    :param body: CommentBase: Pass the updated comment text to the function
    :param db: Session: Access the database
    :param user: User: Check if the user is an admin or moderator,
    :return: A comment or none if the comment_id is invalid
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        if user.role in [UserRole.Admin, UserRole.Moderator] or comment.user_id == user.id:
            comment.comment_text = body.comment_text
            comment.updated_at = func.now()
            db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User) -> Comment | None:
    """
    The delete_comment function deletes a comment from the database.

    :param comment_id: int: Find the comment to delete
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is an admin or moderator
    :return: The deleted comment if it exists, and none otherwise
    """
    if user.role not in [UserRole.Admin, UserRole.Moderator]:
        return
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def get_all_user_comments(skip: int, limit: int, user_id: int, db: Session) -> List[Comment] | None:

    """
    The get_all_user_comments function returns a list of comments made by the user with the given id.
    The function takes in three parameters: skip, limit, and user_id.
    Skip is an integer that determines how many comments to skip before returning results.
    Limit is an integer that determines how many results to return after skipping a certain number of comments (determined by skip).
    User_id is an integer that represents the id of the user whose comments are being returned.

    :param skip: int: Skip the first n comments
    :param limit: int: Limit the number of comments returned
    :param user_id: int: Filter the comments by user_id
    :param db: Session: Pass the database session to the function
    :return: A list of comments that belong to a specific user

    """
    return db.query(Comment).filter(Comment.user_id == user_id).offset(skip).limit(limit).all()


async def get_comments_by_image_id (skip: int, limit: int, image_id: int, db: Session) -> List[Comment] | None:

    """
    The get_comments_by_image_id function returns a list of comments associated with the image_id provided.
    The skip and limit parameters are used to paginate through the results.

    :param skip: int: Skip a number of comments in the database
    :param limit: int: Limit the number of comments returned
    :param image_id: int: Filter the comments by image_id
    :param db: Session: Pass the database session to the function
    :return: A list of comments for a particular image

    """
    return db.query(Comment).filter(Comment.image_id == image_id).offset(skip).limit(limit).all()
