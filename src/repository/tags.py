from src.schemas import TagModel
from src.database.models import Tag
from sqlalchemy.orm import Session


def parse_tags(tags_string: str):
    """
    parse a list of tags

    :param tags_string: string to parse
    :type tags_string: str
    :return: list of tags
    :rtype: List
    """
    result = []
    raw_tag = tags_string.split(' ')
    for cur_tag in raw_tag:
        if cur_tag[:1] == '#':
            result.append(cur_tag[1:])
    return result

async def create_tag(tags_string, db: Session):
    """
    Create a new tags in database just if not exist
    :param tags_string: string to parse
    :type tags_string: str
    :param db: current session to db
    :type db: Session access to database
    :return: List[Tag]
    :rtype: Tag

    """
    result = []
    rw_tags = parse_tags(tags_string=tags_string)
    for tag_name in rw_tags:
        tag = find_tag(tag_name, db)
        if tag:
            result.append(tag)
        else:
            tag = Tag(tag_name=tag_name)
            db.add(tag)
            result.append(tag)
            db.commit()
            db.refresh(tag)
    return result


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

