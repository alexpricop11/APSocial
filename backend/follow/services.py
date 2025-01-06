from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.future import select

from database.database import AsyncSession
from follow.models import Follow
from follow.schemas import FollowRequest
from users.models import User


class FollowService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def follow_user(self, current_user: User, user_id):
        if user_id == current_user.id:
            raise HTTPException(status_code=400, detail="You cannot follow yourself")
        user_to_follow = await self.db.get(User, user_id)
        if not user_to_follow:
            raise HTTPException(status_code=404, detail="User not found")
        result = await self.db.execute(
            select(Follow).filter_by(follower_id=current_user.id, following_id=user_id)
        )
        follow = result.scalar_one_or_none()
        if follow:
            await self.db.delete(follow)
            current_user.following_count -= 1
            user_to_follow.followers_count -= 1
            self.db.add(current_user)
            self.db.add(user_to_follow)
            await self.db.commit()
            return {"detail": "Successfully unfollowed the user"}
        new_follow = Follow(follower_id=current_user.id, following_id=user_id)
        self.db.add(new_follow)
        current_user.following_count += 1
        user_to_follow.followers_count += 1
        self.db.add(current_user)
        self.db.add(user_to_follow)
        await self.db.commit()
        await self.db.refresh(new_follow)
        return {"detail": "Successfully followed the user"}
