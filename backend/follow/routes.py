from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from database.database import get_db
from follow.schemas import FollowRequest
from follow.services import FollowService
from users.auth.jwt import get_current_user
from users.models import User
from follow.models import Follow

follows = APIRouter(tags=['follow'])


@follows.post("/follow/{user_id}")
async def follow_user(
        follow_request: FollowRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    follow_service = FollowService(db)
    return await follow_service.follow_user(current_user, follow_request.user_id)
