from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query, UploadFile, File
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
async def create_image(body: ImageModel,
                       file: UploadFile = File(),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    file_name = CloudImage.generate_name_image()
    CloudImage.upload(file.file, file_name)
    image_url = CloudImage.get_url_for_image(file_name)
    image = await repository_images.create(body, image_url, current_user, db)
    return image
