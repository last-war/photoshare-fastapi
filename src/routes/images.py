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
                     db: Session = Depends(get_db)):
    """
    The get_images function returns a list of images.

    :param limit: int: Limit the number of images returned
    :param le: Limit the number of images returned
    :param offset: int: Skip the first n images
    :param db: Session: Pass the database session to the get_image function
    :return: A list of images
    :doc-author: Trelent
    """
    images = await repository_images.get_images(limit, offset, db)
    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return images


@router.get("/{image_id}", response_model=ImageResponse)
async def get_images(image_id: int = Path(ge=1),
                     db: Session = Depends(get_db)):
    """
    The get_images function returns a list of images.

    :param image_id: int: Specify the id of the image to be retrieved
    :param db: Session: Pass the database session to the function
    :return: A single image
    :doc-author: Trelent
    """
    image = await repository_images.get_image(image_id, db)
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


# @router.patch("/description_{images_id}")
# async def update_description_image(image_id: int = Path(ge=1),
#                                    description: str = ImageModel,
#                                    current_user: User = Depends(auth_service.get_current_user),
#                                    db: Session = Depends(get_db)):
#     pass
