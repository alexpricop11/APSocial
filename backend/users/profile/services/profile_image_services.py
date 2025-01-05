from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.models import User
from users.profile.profile_image_func import validate_image_file, read_image_contents, validate_image_size, \
    convert_image_to_base64, get_user_by_id, update_user_profile_image
from users.profile.schemas import UserProfile


class ProfileImageServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_profile_image(self, user_id: UUID, image: UploadFile):
        try:
            validate_image_file(image)
            contents = await read_image_contents(image)
            validate_image_size(contents)
            image_url = convert_image_to_base64(image, contents)
            user = await get_user_by_id(self.db, user_id)
            await update_user_profile_image(self.db, user, image_url)
            return UserProfile.from_orm(user)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update profile image: {str(e)}")

    async def delete_profile_image(self, user_id: UUID):
        query = select(User).where(user_id == User.id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.profile_image = None
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return {"message": "Profile image deleted successfully"}
