from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from src.database.models import User, Image
from src.repository.tags import create_tags
from src.schemas.images import ImageModel


async def get_images(limit: int, offset: int, user: User, db: Session) -> List[Image] | None:
    """
    The get_images function returns a list of images for the specified user.
        The limit and offset parameters are used to paginate the results.

    Arguments:
        limit (int): maximum number to retrieve
        offset (int): number of object to skip in the search
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        List[Image] | None: A list of image objects or None if no matching images were found
    """
    images = db.query(Image).filter(and_(Image.user_id == user.id, Image.is_deleted == False)).\
        order_by(desc(Image.created_at)).limit(limit).offset(offset).all()
    return images


async def get_image(image_id: int, user: User, db: Session) -> Image | None:
    """
    The get_image function takes in an image_id, a user object and a database session.
    It then queries the database for an image with the given id that belongs to the given user.
    If such an image exists, it is returned.

    Arguments:
        image_id (int): Specify the image id of the image that we want to get
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image | None: Image objects or None if no matching image were found
    """
    image = db.query(Image).filter(and_(Image.user_id == user.id, Image.id == image_id, Image.is_deleted == False)).\
        order_by(desc(Image.created_at)).first()
    return image


async def create(body: ImageModel, image_url: str, user: User, db: Session) -> Image:
    """
    The create function creates a new image in the database.

    Args:
        body (ImageModel): The ImageModel object to be created.
        image_url(str): Pass the image url to the database
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image: The image object
    """
    image = Image(description=body.description, user=user, image_url=image_url, tags=await create_tags(body.tags_text, db))
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_image_from_id(image_id: int, user: User, db: Session) -> Image | None:
    """
    The get_image_from_id function takes in an image_id and a user, and returns the image with that id.

    Args:
        image_id (int): The id of the desired Image object.
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image | None: An image from the database based on an id and a user or None if no matching image were found
    """
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id, Image.is_deleted == False)).first()
    return image


async def get_image_from_url(image_url: str, user: User, db: Session) -> Image | None:
    """
    The get_image_from_url function takes in an image_url and a user object, and returns the Image object
        associated with that url. If no such image exists, it returns None.

    Args:
        image_url(str): Pass the image url to the database
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image | None: The image with the given url and user or None if no matching image were found
    """
    image = db.query(Image).filter(and_(Image.image_url == image_url,
                                        Image.user_id == user.id,
                                        Image.is_deleted == False)).first()
    return image


async def remove(image_id: int, user: User, db: Session) -> Image | None:
    """
    The remove function is used to delete an image from the database.
        It takes in a user and an image_id, and returns the deleted image if it exists.

    Args:
        image_id (int): The id of the desired Image object.
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image | None: the Image object representing the deleted image,
        or None if the user have no permission to delete the image or if no matching image exists in the database
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        image.is_deleted = True
        db.commit()
    return image


async def change_description(body: ImageModel, image_id: int, user: User, db: Session) -> Image | None:
    """
    The change_description function takes in a body, image_id, user and db.
        The function then gets the image from the id provided by the user.
        If there is an image it changes its description to what was provided in the body.

    Args:
        body (ImageModel): The ImageModel object to be created.
        image_id(int): The id of the desired Image object.
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image: The image object with the updated description
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        image.description = body.description
        db.commit()
    return image
