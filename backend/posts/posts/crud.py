import os
import shutil
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from posts.posts.models import Post
from posts.posts.schemas import PostCreate


async def create_posts(db: AsyncSession, image: PostCreate) -> Post:
    os.makedirs("uploads", exist_ok=True)
    file_name = f"{uuid4()}.jpg"
    file_location = f"uploads/{file_name}"
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.image.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")
    post = Post(image=file_location, user=image.user_id, uploaded_at=image.uploaded_at)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_posts_by_id(db: AsyncSession, user_id: UUID):
    result = await db.execute(
        select(Post)
        .filter(user_id == Post.user)
        .order_by(desc(Post.uploaded_at)))
    posts = result.scalars().all()
    return posts


async def delete_image(db: AsyncSession, user, image_id: int) -> bool:
    result = await db.execute(select(Post).filter(image_id == Post.id, user.id == Post.user))
    post = result.scalar_one_or_none()
    if post:
        if os.path.exists(post.image):
            os.remove(post.image)
        await db.delete(post)
        await db.commit()
        return True
    return False
