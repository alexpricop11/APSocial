from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from posts.images.crud import create_posts
from posts.images.schemas import PostCreate
from users.auth.jwt import get_current_user
from users.models import User

posts = APIRouter(tags=['posts'])


@posts.post('/create-post')
async def create_post(
        image: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    post_create = PostCreate(
        user_id=current_user.id,
        image=image,
        uploaded_at=datetime.utcnow()
    )
    db_image = await create_posts(db=db, image=post_create)
    return db_image

@posts.get('/posts')
async def get_posts():
    ...