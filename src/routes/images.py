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
    file_name = CloudImage.generate_name_image()
    CloudImage.upload(image_file.file, file_name)
    image_url = CloudImage.get_url_for_image(file_name)
    body = ImageModel(description=description)
    image = await repository_images.create(body, image_url, current_user, db)
    return image


@router.get("/", response_model=List[ImageResponse])
async def get_images(limit: int = Query(10, le=50), offset: int = 0,
                     current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    images_url = await repository_images.get_images(limit, offset, current_user, db)
    return images_url


# @router.get("/{image_id}", response_model=)
# async def get_images(image_id: int = Path(ge=1),
#                      current_user: User = Depends(auth_service.get_current_user),
#                      db: Session = Depends(get_db)):
#     images_url = await repository_images.get_images(limit, offset, current_user, db)
#     return images_url


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_image(image_id: int = Path(ge=1),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
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