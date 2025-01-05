from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from posts.likes.repository import LikeRepository
from posts.likes.services import LikeService

like = APIRouter(tags=['likes'])


@like.post("/likes/toggle")
async def toggle_like(
        user_id: UUID,
        target_type: str,
        target_id: int,
        db: AsyncSession = Depends(get_db)
):
    like_repository = LikeRepository(db)
    like_service = LikeService(like_repository)

    result = await like_service.toggle_like(user_id, target_type, target_id)
    if result:
        return result
    else:
        return {"message": "Like removed"}
