from fastapi import APIRouter, Depends, status, HTTPException

from src.database.models import User
from src.repository import tags as repository_tag
from src.schemas import TagResponse, TagModel
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.services.auth import auth_service


router = APIRouter(prefix='/tag', tags=['tags'])


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(body: TagModel,
                     cur_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    create new tag from tag_name

    :param body: all need field to create
    :type body: TagModel
    :param cur_user: get the user who is making the request
    :type cur_user: User
    :param db: current session to db
    :type db: Session access to database
    :return: tag object
    :rtype: Tag | None
    """
    tag = await repository_tag.create_tag(body, cur_user, db)
    return tag


@router.get("/{tag_name}", response_model=TagResponse)
async def get_one(tag_name: str,
                  cur_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    route to get tag object by tag name

    :param tag_name: tag name to found
    :type tag_name: str
    :param cur_user: get the user who is making the request
    :type cur_user: User
    :param db: current session to db
    :type db: Session access to database
    :return: tag object
    :rtype: Tag | None
    """
    tag = await repository_tag.find_tag(tag_name, cur_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return tag


@router.put("/{tag_name}", response_model=TagResponse)
async def update_tag(body: TagModel, cur_user: User = Depends(auth_service.get_current_user),
                 db: Session = Depends(get_db)):
    """
    update tag finded by tag name

    :param body: all need field to update
    :type body: TagModel
    :param cur_user: get the user who is making the request
    :type cur_user: User
    :param db: current session to db
    :type db: Session access to database
    :return: tag object
    :rtype: Tag | None
    """

    tag = await repository_tag.edit_tag(body, cur_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return tag


@router.delete("/{tag_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(tag_name: str, cur_user: User = Depends(auth_service.get_current_user),
                 db: Session = Depends(get_db)):
    """
    route to delete tag finded by name

    :param tag_name: tag to found
    :type tag_name: str
    :param cur_user: get the user who is making the request
    :type cur_user: User
    :param db: current session to db
    :type db: Session access to database
    :return: tag object
    :rtype: Tag | None
    """
    tag = await repository_tag.delete_tag(tag_name, cur_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return tag

