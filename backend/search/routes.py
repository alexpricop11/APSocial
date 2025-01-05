from typing import List

from fastapi import APIRouter, Depends

from database.database import AsyncSession, get_db
from search.schemas import ResultSearch
from search.services import SearchService
from users.auth.jwt import get_current_user
from users.models import User

search = APIRouter(tags=['search'])


@search.get('/search', response_model=List[ResultSearch])
async def search_user(
        query: str,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    search_service = SearchService(db)
    users = await search_service.search_user(query, user.id)
    return users
