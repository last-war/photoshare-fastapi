from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.models import User, Comment, UserRole
from src.schemas import CommentBase


async def create_comment(image_id: int, body: CommentBase, db: Session, user: User) -> Comment:
    comment = Comment(user_id=user.id,
                      image_id=image_id,
                      created_at=func.now(),
                      comment_text=body.comment_text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def edit_comment(comment_id: int, body: CommentBase, db: Session, user: User) -> Comment | None:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        if user.role in [UserRole.Admin, UserRole.Moderator] or comment.user_id == user.id:
            comment.comment_text = body.comment_text
            comment.updated_at = func.now()
            db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User):
    if user.role not in [UserRole.Admin, UserRole.Moderator]:
        return
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def get_all_user_comments(user_id: int, db: Session) -> List[Comment] | None:
    return db.query(Comment).filter(Comment.user_id == user_id).all()
