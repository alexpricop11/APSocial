from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from users.auth.jwt import get_current_user
from users.models import User
from users.profile.schemas import EditProfile
from users.profile.services import UserProfileServices

user = APIRouter(tags=['profile'])


@user.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    profile_service = UserProfileServices(db)
    return await profile_service.get_user_profile(current_user.id)


# TODO sa se rezolve problema cu schimbarea imaginii de profil
@user.post('/edit-profile')
async def edit_profile(
        profile_data: EditProfile,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    profile_service = UserProfileServices(db)
    return await profile_service.edit_profile(current_user.id, profile_data)


# TODO sa se rezolve problema cu schimbarea imaginii de profil
@user.post("/user/profile/image")
async def update_profile_image(
        image: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not image.content_type.startswith('images/'):
        raise HTTPException(status_code=400, detail="File must be an images")

    service = UserProfileServices(db)
    return await service.update_profile_image(current_user.id, image)
