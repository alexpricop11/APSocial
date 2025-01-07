from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.database import AsyncSession
from follow.models import Follow
from follow.schemas import FollowList
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
        else:
            new_follow = Follow(follower_id=current_user.id, following_id=user_id)
            self.db.add(new_follow)
            current_user.following_count += 1
            user_to_follow.followers_count += 1
        self.db.add(current_user)
        self.db.add(user_to_follow)
        await self.db.commit()
        return {"detail": "Successfully followed/unfollowed the user"}

    async def get_followers(self, user_id: UUID):
        query = select(Follow).options(joinedload(Follow.follower)).where(user_id == Follow.following_id)
        result = await self.db.execute(query)
        followers = result.scalars().all()
        return [
            FollowList(
                id=follower.follower.id,
                username=follower.follower.username,
                profile_image=follower.follower.profile_image
            ) for follower in followers
        ]

    async def get_following(self, user_id: UUID):
        query = select(Follow).options(joinedload(Follow.following)).where(user_id == Follow.follower_id)
        result = await self.db.execute(query)
        following = result.scalars().all()

        return [
            FollowList(
                id=follow.following.id,
                username=follow.following.username,
                profile_image=follow.following.profile_image
            ) for follow in following
        ]
