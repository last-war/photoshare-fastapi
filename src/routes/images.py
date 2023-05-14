from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query, UploadFile, File, Body, Form
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ImageModel, ImageResponse
from src.repository import images as repository_images
from src.services.cloud_image import CloudImage
from src.services.auth import auth_service


"""
Routes image.
"""


router = APIRouter(prefix="/images", tags=['images'])


@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(description: str = Form(),
                       # TODO tags:
                       image_file: UploadFile = File(),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    The create_image function creates a new image in the database.

    :param description: str: Get the description of the image from the form
    :param # TODO tags:
                           image_file: UploadFile: Upload the image file to the cloud
    :param current_user: User: Get the user who is currently logged in
    :param db: Session: Pass the database session to the repository function
    :return: A new image
    :doc-author: Trelent
    """
    file_name = CloudImage.generate_name_image()
    CloudImage.upload(image_file.file, file_name, overwrite=False)
    image_url = CloudImage.get_url_for_image(file_name)
    body = ImageModel(description=description)
    image = await repository_images.create(body, image_url, current_user, db)
    return image


@router.get("/", response_model=List[ImageResponse])
async def get_images(limit: int = Query(10, le=50), offset: int = 0,
                     current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    """
    The get_images function returns a list of images.

    :param limit: int: Limit the number of images returned
    :param le: Limit the number of images returned to 50
    :param offset: int: Specify the number of records to skip before returning results
    :param current_user: User: Get the current user from the database
    :param db: Session: Get a database session
    :return: A list of images
    :doc-author: Trelent
    """
    images = await repository_images.get_images(limit, offset, current_user, db)
    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return images


@router.get("/{image_id}", response_model=ImageResponse)
async def get_images(image_id: int = Path(ge=1),
                     current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    """
    The get_images function is a GET request that returns the image with the given ID.
    The function takes an optional image_id parameter, which defaults to 1 if not provided.
    It also takes a current_user parameter, which is obtained from auth_service and db parameters,
    which are obtained from get_db.

    :param image_id: int: Specify the id of the image that is being requested
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository
    :return: A list of images
    :doc-author: Trelent
    """
    image = await repository_images.get_image(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return image


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_image(image_id: int = Path(ge=1),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    The remove_image function removes an image from the database.

    :param image_id: int: Specify the id of the image to be removed
    :param current_user: User: Get the user_id of the logged in user
    :param db: Session: Access the database
    :return: The image that was removed
    :doc-author: Trelent
    """
    image = await repository_images.remove(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return image


@router.patch("/description/{image_id}", response_model=ImageResponse)
async def update_description_image(body: ImageModel,
                                   image_id: int = Path(ge=1),
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)):
    """
    The update_description_image function updates the description of an image.
        The function takes in a body, which is an ImageModel object, and an image_id.
        It also takes in a current_user and db objects as dependencies.

    :param body: ImageModel: Get the new description for the image
    :param image_id: int: Get the image id from the path
    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the repository
    :return: The updated image
    :doc-author: Trelent
    """
    image = await repository_images.change_description(body, image_id, current_user, db)
    if image is None or image.is_deleted is True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return image
