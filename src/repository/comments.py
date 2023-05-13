from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.models import User, Comment, UserRole
from src.schemas import CommentBase


async def create_comment(image_id: int, body: CommentBase, db: Session, user: User) -> Comment:
    """
    The create_comment function creates a new comment in the database.
    Args:
    image_id (int): The id of the image to which this comment belongs.
    body (CommentBase): The request body containing information about the new comment.
    db (Session): A database session object used for querying and modifying data in our database.

    :param image_id: int: Specify the image that the comment is being made on
    :param body: CommentBase: Pass the comment_text from the request body to the function
    :param db: Session: Access the database
    :param user: User: Get the user id from the token
    :return: A comment object
    :doc-author: Trelent
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
    :doc-author: Trelent
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
    Args:
    comment_id (int): The id of the comment to be deleted.
    db (Session): A connection to the database.
    user (User): The user who is deleting this post, must be an admin or moderator.

    :param comment_id: int: Find the comment to delete
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is an admin or moderator
    :return: The deleted comment if it exists, and none otherwise
    :doc-author: Trelent
    """
    if user.role not in [UserRole.Admin, UserRole.Moderator]:
        return
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def get_all_user_comments(user_id: int, db: Session) -> List[Comment] | None:
    """
    The get_all_user_comments function returns a list of all comments made by the user with the given id.
    If no such user exists, None is returned.

    :param user_id: int: Filter the comments by user_id
    :param db: Session: Get the database session
    :return: A list of comments that belong to a particular user
    :doc-author: Trelent
    """
    return db.query(Comment).filter(Comment.user_id == user_id).all()


async def get_comments_by_image_id(image_id: int, db: Session) -> List[Comment] | None:
    """
    The get_comments_by_image_id function takes in an image_id and a database session,
    and returns all comments associated with the given image_id. If no comments are found,
    the function returns None.

    :param image_id: int: Filter the comments by image_id
    :param db: Session: Pass in the database session
    :return: A list of comments associated with a specific image
    :doc-author: Trelent
    """
    return db.query(Comment).filter(Comment.image_id == image_id).all()
