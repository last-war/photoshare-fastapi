from fastapi import APIRouter, Depends, status, HTTPException

from src.database.models import User, UserRole
from src.repository import ratings as repository_ratings
from src.schemas import RatingResponse, RatingModel
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.services.roles import RoleAccess

router = APIRouter(prefix='/rating', tags=['ratings'])

allowed_operation_get = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_post = RoleAccess([UserRole.Admin, UserRole.Moderator, UserRole.User])
allowed_operation_put = RoleAccess([UserRole.Admin, UserRole.Moderator])
allowed_operation_delete = RoleAccess([UserRole.Admin, UserRole.Moderator])


