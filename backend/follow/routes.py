from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from follow.schemas import FollowRequest, FollowersList, FollowingList
from follow.services import FollowService
from users.auth.jwt import get_current_user
from users.models import User

follows = APIRouter(tags=['follow'])


@follows.post("/follow/{user_id}")
async def follow_user(
        follow_request: FollowRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    follow_service = FollowService(db)
    return await follow_service.follow_user(current_user, follow_request.user_id)


@follows.get("/followers", response_model=FollowersList)
async def get_followers(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    follow_service = FollowService(db)
    followers_list = await follow_service.get_followers(current_user.id)
    return {"followers": followers_list}


@follows.get("/following", response_model=FollowingList)
async def get_following(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    follow_service = FollowService(db)
    following_list = await follow_service.get_following(current_user.id)
    return {"following": following_list}
