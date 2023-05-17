from typing import List

from sqlalchemy import and_, desc

from src.schemas.schemas import TagModel
from src.database.models import Tag, tag_to_image, Image
from sqlalchemy.orm import Session


def parse_tags(tags_string: str) -> list[str]:
    """
    parse a list of tags

    :param tags_string: str: string to parse
    :return: list of tags
    """
    result = []
    raw_tag = tags_string.split(' ')
    for cur_tag in raw_tag:
        if cur_tag[:1] == '#':
            result.append(cur_tag[1:])
    return result


async def create_tags(tags_string, db: Session) -> List[Tag]:
    """
    Create a new tags in database just if not exist
    limit 5 tags

    :param tags_string: str: string to parse
    :param db: Session: current session to db
    :return: List[Tag]

    """
    result = []
    rw_tags = parse_tags(tags_string)
    for tag_name in rw_tags:
        if result.count() == 5:
            return result
        tag = find_tag(tag_name, db)
        if tag:
            result.append(tag)
        else:
            tag = Tag(tag_name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
            result.append(tag)
    return result


async def edit_tag(body: TagModel, db: Session) -> Tag | None:
    """
    get tag from database by name

    :param body: TagModel: request body containing information about tag for editing
    :param db: Session: current session to db
    :return: tag object
    """
    tag = db.query(Tag).filter(Tag.tag_name == body.tag_name).first()
    return tag


async def find_tag(tag_name: str, db: Session) -> Tag | None:
    """
    get tag from database by name

    :param tag_name: str: name to find
    :param db: Session: current session to db
    :return: tag object
    """
    tag = db.query(Tag).filter(Tag.tag_name == tag_name).first()
    return tag


async def delete_tag(tag_name: str, db: Session) -> Tag | None:
    """
    Delete tag from database just for Administrator role

    :param tag_name: str: name to find tag
    :param db: Session: current session to db
    :return: The deleted tag if found in database
    """
    tag = find_tag(tag_name, db)
    db.add(tag)
    if tag:
        db.delete(tag)
        db.commit()
    return tag


async def get_images_by_tag(tag: str, limit: int, offset: int, db: Session) -> List[Image]:
    """
    The get_images function returns a list of images for the specified user.
        The limit and offset parameters are used to paginate the results.

    :param tag: str: tag to filter the images
    :param limit: int: Limit the number of images returned
    :param offset: int: Specify the offset of the images to be retrieved
    :param db: Session: Pass the database session to the function
    :return: A list of image objects
    """
    tag_db = db.query(Tag).filter(Tag.tag_name == tag).first()
    images_ids = db.query(tag_to_image).filter(Tag.id == tag_db.id).all()
    images = db.query(Image).filter(and_(Image.id.in_(images_ids), Image.is_deleted == False)).\
        order_by(desc(Image.created_at)).limit(limit).offset(offset).all()
    return images
