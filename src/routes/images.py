from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from src.database.db import get_db
from src.database.models import User, UserRole
from src.schemas import ImageModel, ImageResponse, ImageTransformationModel
from src.repository import images as repository_images
from src.services.cloud_image import CloudImage
from src.services.auth import auth_service
from src.services.roles import RoleAccess


"""
Routes image.
"""


router = APIRouter(prefix="/images", tags=['images'])

allowed_operation_get = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_post = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_patch = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_put = RoleAccess([UserRole.Admin, UserRole.Moderator])
allowed_operation_delete = RoleAccess([UserRole.Admin])


@router.post("/", response_model=ImageResponse, dependencies=[Depends(allowed_operation_post)],
             status_code=status.HTTP_201_CREATED)
async def create_image(description: str = Form(),
                       tags_text: str = Form(),
                       image_file: UploadFile = File(),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    """
    The create_image function creates a new image in the database.

    :param description: str: Get the description of the image from the form
    :param tags_text: str: optional string with the tags
    :param image_file: UploadFile: Upload the image file to the cloud
    :param current_user: User: Get the user who is currently logged in
    :param db: Session: Pass the database session to the repository function
    :return: A new image
    """
    file_name = CloudImage.generate_name_image()
    CloudImage.upload(image_file.file, file_name, overwrite=False)
    image_url = CloudImage.get_url_for_image(file_name)
    body = ImageModel(description=description, tags=tags_text)
    image = await repository_images.create(body, image_url, current_user, db)
    return image


@router.post("/transformation", response_model=ImageResponse, dependencies=[Depends(allowed_operation_post)],
             status_code=status.HTTP_201_CREATED)
async def create_transformation_image(body: ImageTransformationModel,
                                      current_user: User = Depends(auth_service.get_current_user),
                                      db: Session = Depends(get_db)):
    """
    The create_transformation_image function creates a new image transformation.
        The function takes in the following parameters:
            body (ImageTransformationModel): A JSON object containing the id of an existing image and a string representing
                the desired transformation to be applied to that image. The possible transformations are as follows:
                    &quot;blur&quot;, &quot;brightness&quot;, &quot;contrast&quot;, &quot;crop_center&quot;, &quot;flip_horizontal&quot; ,
                    &quot;flip_vertical&quot; ,  	&quot;grayscale&quot; ,  	&quot;invert&quot;,&quot;pixelate&quot;,&quot;rotate90&quot;,&quot;rotate180&quot;,&quot;rotate270&quot;.

    :param body: ImageTransformationModel: Get the id of the image to transform and
    :param current_user: User: Get the current user from the database
    :param db: Session: Access the database
    :return: The image that was created
    """
    image = await repository_images.get_image_from_id(body.id, current_user, db)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    transformation_image_url = CloudImage.get_transformation_image(image.image_url, body.transformation)
    body = ImageModel(description=image.description)
    image_in_db = await repository_images.get_image_from_url(transformation_image_url, current_user, db)
    if image_in_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Resource already exists")
    new_image = await repository_images.create(body, transformation_image_url, current_user, db)
    return new_image


@router.get("/", response_model=List[ImageResponse], dependencies=[Depends(allowed_operation_get)])
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
    """
    images = await repository_images.get_images(limit, offset, current_user, db)
    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return images


@router.get("/{image_id}", response_model=ImageResponse, dependencies=[Depends(allowed_operation_get)])
async def get_image(image_id: int = Path(ge=1),
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


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_delete)])
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


@router.patch("/description/{image_id}", response_model=ImageResponse, dependencies=[Depends(allowed_operation_patch)])
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


@router.post("/generate_qrcode/{image_id}", dependencies=[Depends(allowed_operation_post)])
async def generate_qrcode(image_id: int = Path(ge=1),
                          current_user: User = Depends(auth_service.get_current_user),
                          db: Session = Depends(get_db)):
    """
    The generate_qrcode function generates a QR code for the image with the given ID.

    :param image_id: int: Get the image from the database
    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: A streamingresponse
    :doc-author: Trelent
    """
    image = await repository_images.get_image(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    qr_code = await CloudImage.create_qr_code_image(image.image_url)
    if qr_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return StreamingResponse(qr_code, media_type="image/png", status_code=status.HTTP_201_CREATED)
