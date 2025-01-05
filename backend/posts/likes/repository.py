from uuid import UUID

from sqlalchemy.future import select

from database.database import AsyncSession
from posts.likes.models import Like
from posts.likes.schemas import LikeCreate


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_like(self, like: LikeCreate) -> Like:
        db_like = Like(**like.dict())
        self.db.add(db_like)
        await self.db.commit()
        await self.db.refresh(db_like)
        return db_like

    async def get_like_target(self, user_id : UUID, target_type: str, target_id: int) -> Like:
        result = await self.db.execute(
            select(Like).filter(
                user_id == Like.user_id,
                target_type == Like.target_type,
                target_id == Like.target_id
            )
        )
        return result.scalars().first()

    async def delete_like(self, like: Like):
        await self.db.delete(like)
        await self.db.commit()
