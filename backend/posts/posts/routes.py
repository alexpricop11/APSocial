from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from posts.posts.crud import create_posts, get_posts_by_id, delete_image
from posts.posts.schemas import PostCreate, PostInDB
from users.auth.jwt import get_current_user
from users.models import User

post = APIRouter(tags=['posts'])


@post.post('/create-post')
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


@post.get('/get-posts')
async def get_posts(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    posts = await get_posts_by_id(db, current_user.id)
    if not posts:
        return []
    return posts


@post.delete('/delete-posts/{post_id}')
async def delete_post(
        post_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await delete_image(db, current_user.id, post_id)
    return {"message": "The post deleted successfully."}
