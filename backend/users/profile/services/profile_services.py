from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from users.models import User
from users.profile.schemas import UserProfile, EditProfile, OtherUserProfile


class UserProfileServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_profile(self, user_id: UUID) -> UserProfile:
        query = select(User).where(user_id == User.id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')
        return UserProfile.from_orm(user)

    async def get_other_profile(self, user_id: UUID) -> OtherUserProfile:
        query = select(User).where(user_id == User.id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return OtherUserProfile.from_orm(user)

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
