from uuid import UUID

from sqlalchemy.future import select

from database.database import AsyncSession
from users.models import User


class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_user(self, query: str, my_user: UUID):
        users = select(User).where(
            User.username.ilike(f'%{query}%'),
            my_user != User.id
        )
        result = await self.db.execute(users)
        return result.scalars().all()
