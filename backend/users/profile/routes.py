from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from users.auth.jwt import get_current_user
from users.models import User
from users.profile.schemas import EditProfile
from users.profile.services.profile_image_services import ProfileImageServices
from users.profile.services.profile_services import UserProfileServices

user = APIRouter(tags=['profile'])


@user.get("/profile")
async def get_profile(
        current_user: dict | User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    profile_service = UserProfileServices(db)
    if isinstance(current_user, dict) and "new_token" in current_user:
        users = current_user["user"]
        new_token = current_user["new_token"]
        profile = await profile_service.get_user_profile(users.id)
        return {"profile": profile, "new_token": new_token}
    else:
        profile = await profile_service.get_user_profile(current_user.id)
        return {"profile": profile}


@user.get('/profile/{user_id}')
async def get_other_user_profile(
        user_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    profile_service = UserProfileServices(db)
    try:
        profile = await profile_service.get_other_profile(user_id)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")


@user.post('/edit-profile')
async def edit_profile(
        profile_data: EditProfile,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    profile_service = UserProfileServices(db)
    return await profile_service.edit_profile(current_user.id, profile_data)


@user.post("/user/profile/image")
async def update_profile_image(
        image: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    service = ProfileImageServices(db)
    return await service.update_profile_image(current_user.id, image)


@user.delete("/user/profile/image")
async def delete_profile_image(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    service = ProfileImageServices(db)
    return await service.delete_profile_image(current_user.id)
