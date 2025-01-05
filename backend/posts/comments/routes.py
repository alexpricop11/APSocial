from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db

from users.auth.jwt import get_current_user
from users.models import User

comment = APIRouter(tags=['comments'])
