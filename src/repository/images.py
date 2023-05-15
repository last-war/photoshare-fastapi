from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from src.database.models import User, Image
from src.repository.tags import connect_tag
from src.schemas import ImageModel


"""
Asynchronous functions for interaction with the database with the images table.
"""


async def get_images(limit: int, offset: int, user: User, db: Session):
    """
    The get_images function returns a list of images for the specified user.
        The limit and offset parameters are used to paginate the results.


    :param limit: int: Limit the number of images returned
    :param offset: int: Specify the offset of the images to be retrieved
    :param user: User: Get the images of a specific user
    :param db: Session: Pass the database session to the function
    :return: A list of image objects
    """
    images = db.query(Image).filter(and_(Image.user_id == user.id, Image.is_deleted == False)).\
        order_by(desc(Image.created_at)).limit(limit).offset(offset).all()
    return images


async def get_image(image_id: int, user: User, db: Session):
    """
    The get_image function takes in an image_id, a user object and a database session.
    It then queries the database for an image with the given id that belongs to the given user.
    If such an image exists, it is returned.

    :param image_id: int: Specify the image id of the image that we want to get
    :param user: User: Get the user object from the database
    :param db: Session: Access the database
    :return: The image with the id and user_id that is given in the arguments
    """
    image = db.query(Image).filter(and_(Image.user_id == user.id, Image.id == image_id, Image.is_deleted == False)).\
        order_by(desc(Image.created_at)).first()
    return image


async def create(body: ImageModel, image_url: str, user: User, db: Session):
    """
    The create function creates a new image in the database.
        Args:
            body (ImageModel): The ImageModel object to be created.
            user (User): The User object that is creating the image.
            db (Session): A connection to the database session.

    :param body: ImageModel: Get the data from the request body
    :param image_url: str: Pass the image url to the database
    :param user: User: Get the user who is logged in
    :param db: Session: Access the database
    :return: The image object
    """
    image = Image(**body.dict(), user=user, image_url=image_url, tags=create_tags(body.tags, db))
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_image_from_id(image_id: int, user: User, db: Session):
    """
    The get_image_from_id function takes in an image_id and a user, and returns the image with that id.
        Args:
            image_id (int): The id of the desired Image object.
            user (User): The User object associated with the desired Image object.

    :param image_id: int: Specify the image id of the image we want to get from our database
    :param user: User: Get the user's id and check if they are the owner of the image
    :param db: Session: Communicate with the database
    :return: An image from the database based on an id and a user
    """
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id, Image.is_deleted == False)).first()
    return image


async def get_image_from_url(image_url: str, user: User, db: Session):
    """
    The get_image_from_url function takes in an image_url and a user object, and returns the Image object
        associated with that url. If no such image exists, it returns None.

    :param image_url: str: Specify the image url
    :param user: User: Get the user from the database
    :param db: Session: Access the database
    :return: The image with the given url and user
    """
    image = db.query(Image).filter(and_(Image.image_url == image_url, Image.user_id == user.id)).first()
    return image


async def remove(image_id: int, user: User, db: Session):
    """
    The remove function is used to delete an image from the database.
        It takes in a user and an image_id, and returns the deleted image if it exists.

    :param image_id: int: Get the image object from the database
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: The image that was removed
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        image.is_deleted = True
        db.commit()
    return image


async def change_description(body: ImageModel, image_id: int, user: User, db: Session):
    """
    The change_description function takes in a body, image_id, user and db.
        The function then gets the image from the id provided by the user.
        If there is an image it changes its description to what was provided in the body.

    :param body: ImageModel: Get the description from the request body
    :param image_id: int: Get the image from the database
    :param user: User: Check if the user is authorized to change the description
    :param db: Session: Pass the database session to the function
    :return: The image with the updated description
    """
    image = await get_image_from_id(image_id, user, db)
    if image:
        image.description = body.description
        db.commit()
    return image
