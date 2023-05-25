from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse
from pydantic import ValidationError

from src.database.db import get_db
from src.database.models import User, UserRole
from src.schemas.images import ImageModel, ImageResponse, ImageTransformationModel
from src.repository import images as repository_images
from src.services.cloud_image import CloudImage
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.services.tags import create_transformation_tags

router = APIRouter(prefix="/images", tags=['images'])

allowed_operation_get = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_post = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_patch = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_put = RoleAccess([UserRole.Admin, UserRole.Moderator])
allowed_operation_delete = RoleAccess([UserRole.Admin])


@router.post("/", response_model=ImageResponse, dependencies=[Depends(allowed_operation_post)],
             status_code=status.HTTP_201_CREATED)
async def create_image(description: str = Form(),
                       tags_text: str = Form(None),
                       image_file: UploadFile = File(),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):

    """
    The create_image function creates a new image in the database.

    Arguments:
        description (str): Get the description from the request body
        tags_text (str): Get the tags from the request body
        image_file (UploadFile): Get the file from the request
        current_user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image: the Image object
    """
    try:
        body = ImageModel(description=description, tags_text=tags_text)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="UNPROCESSABLE_ENTITY")
    file_name = CloudImage.generate_name_image()
    CloudImage.upload(image_file.file, file_name, overwrite=False)
    image_url = CloudImage.get_url_for_image(file_name)
    image = await repository_images.create(body, image_url, current_user, db)
    return image


@router.post("/transformation", response_model=ImageResponse, dependencies=[Depends(allowed_operation_post)],
             status_code=status.HTTP_201_CREATED)
async def create_transformation_image(body: ImageTransformationModel,
                                      current_user: User = Depends(auth_service.get_current_user),
                                      db: Session = Depends(get_db)):

    """
    The create_transformation_image function creates a new image in the database.
        The function takes an ImageTransformationModel object as input, which contains the id of the original image and
        transformation to be applied on it. It then uses CloudImage class to get a url for transformed image
        from cloudinary, checks if there is already an entry with that url in database and if not creates one.
        Input examples ->"standard" or "radius" or "grayscale" or "cartoonify" or "vectorize".

    Arguments:
        body (ImageTransformationModel): Get the id of the image that is to be transformed
        current_user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image: new image with the transformation applied
    """
    image = await repository_images.get_image_from_id(body.id, current_user, db)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    transformation_image_url = CloudImage.get_transformation_image(image.image_url, body.transformation)

    tags_in_text = None
    if len(image.tags) > 0:
        tags_in_text = create_transformation_tags(image.tags)

    body = ImageModel(description=image.description, tags_text=tags_in_text)
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

    Arguments:
        limit (int): Limit the number of images returned
        offset (int): Specify the number of records to skip before returning results
        current_user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        List[Image]: A list of images
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

    Arguments:
        image_id (int): Specify the id of the image that is being requested
        current_user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image: image
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

    Arguments:
        image_id (int): Specify the id of the image to be removed
        current_user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        None: The image that was removed
    """
    image = await repository_images.remove(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return None


@router.patch("/description/{image_id}", response_model=ImageResponse, dependencies=[Depends(allowed_operation_patch)])
async def update_description_image(body: ImageModel,
                                   image_id: int = Path(ge=1),
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)):
    """
    The update_description_image function updates the description of an image.
        The function takes in a body, which is an ImageModel object, and an image_id.
        It also takes in a current_user and db objects as dependencies.

    Arguments:
        body (ImageModel): Get the new description for the image
        image_id (int): Get the image id from the path
        current_user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        Image: The updated image
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

    Arguments:
        image_id (int): Get the image id from the path
        current_user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        image/png: streamingresponse
    """
    image = await repository_images.get_image(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    qr_code = await CloudImage.create_qr_code_image(image.image_url)
    if qr_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return StreamingResponse(qr_code, media_type="image/png", status_code=status.HTTP_201_CREATED)
