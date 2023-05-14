from src.schemas import TagModel
from src.database.models import Tag, User, UserRole
from sqlalchemy.orm import Session


async def create_tag(body: TagModel, db: Session):
    """
    Create a new tag in database just if not exist

    :param body: request body containing information about new tag
    :type body: TagModel
    :param db: current session to db
    :type db: Session access to database
    :return: added tag object
    :rtype: Tag | None
    """
    tag = find_tag(body.tag_name, db)
    if tag:
        return tag
    tag = Tag(**body.dict())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def edit_tag(body: TagModel, db: Session) -> Tag | None:
    """
    get tag from database by name

    :param body: request body containing information about tag for editing
    :type body: TagModel
    :param db: current session to db
    :type db: Session access to database
    :return: tag object
    :rtype: Tag | None
    """
    tag = db.query(Tag).filter(Tag.tag_name == body.tag_name).first()
    return tag


async def find_tag(tag_name: str, db: Session) -> Tag | None:
    """
    get tag from database by name

    :param tag_name: name to find
    :type tag_name: str
    :param db: current session to db
    :type db: Session access to database
    :return: tag object
    :rtype: Tag | None
    """
    tag = db.query(Tag).filter(Tag.tag_name == tag_name).first()
    return tag


async def delete_tag(tag_name: str, db: Session) -> Tag | None:
    """
    Delete tag from database just for Administrator role

    :param tag_name: name to find tag
    :type tag_name: str
    :param db: current session to db
    :type db: Session access to database
    :return: The deleted tag if found in database
    :rtype: Tag | None
    """
    tag = find_tag(tag_name, db)
    db.add(tag)
    if tag:
        db.delete(tag)
        db.commit()
    return tag

