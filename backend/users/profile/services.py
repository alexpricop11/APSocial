from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import Users
from users.profile.schemas import UserProfile, EditProfile


class UserProfileServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_profile(self, user_id: UUID) -> UserProfile:
        query = select(Users).where(user_id == Users.id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=400, detail='User not found')
        return UserProfile.from_orm(user)

    async def edit_profile(self, user_id: UUID, profile_data: EditProfile):
        query = select(Users).where(user_id == Users.id)
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
