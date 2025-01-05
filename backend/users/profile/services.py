from uuid import UUID
import base64
from PIL import Image
from io import BytesIO
from fastapi import HTTPException, UploadFile
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.models import User
from users.profile.schemas import UserProfile, EditProfile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserProfileServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_profile(self, user_id: UUID) -> UserProfile:
        query = select(User).where(user_id == User.id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=400, detail='User not found')
        return UserProfile.from_orm(user)

    async def edit_profile(self, user_id: UUID, profile_data: EditProfile):
        query = select(User).where(user_id == User.id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(user)
        except Exception as ex:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(ex)}")
        return UserProfile.from_orm(user)

    async def update_profile_image(self, user_id: UUID, image: UploadFile):
        try:
            if not image.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="File must be an image")

            contents = await image.read()
            if len(contents) > 5 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="Image too large")
            base64_str = base64.b64encode(contents).decode('utf-8')
            mime_type = image.content_type or 'image/png'
            image_url = f"data:{mime_type};base64,{base64_str}"
            query = select(User).where(user_id == User.id)
            result = await self.db.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user.profile_image = image_url
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

            return UserProfile.from_orm(user)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update profile image: {str(e)}")
