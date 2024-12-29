import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from database.database import get_db
from password_service.service import PasswordService
from users.auth.jwt import get_current_user
from users.models import Users
from users.profile.schemas import EditProfile
from users.profile.services import UserProfileServices

user = APIRouter(tags=['profile'])


@user.get("/profile")
async def get_profile(current_user: Users = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    profile_service = UserProfileServices(db)
    return await profile_service.get_user_profile(current_user.id)


@user.post('/edit-profile')
async def edit_profile(
        profile_data: EditProfile,
        current_user: Users = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    profile_service = UserProfileServices(db)
    return await profile_service.edit_profile(current_user.id, profile_data)


UPLOAD_DIR = Path("uploads/profile_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@user.post("/user/profile/image")
async def update_profile_image(
        current_user: Users = Depends(get_current_user),
        image: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    service = UserProfileServices(db)
    image_data = await image.read()
    return await service.update_profile_image(current_user.id, image_data)

