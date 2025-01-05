import os
import shutil
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from posts.images.models import Post
from posts.images.schemas import PostCreate


async def create_posts(db: AsyncSession, image: PostCreate) -> Post:
    os.makedirs("posts", exist_ok=True)
    file_location = f"posts/{uuid4()}.jpg"
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


async def get_posts(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(Post).filter(user_id == Post.user))
    return result.scalars().all()


async def delete_image(db: AsyncSession, image_id: int) -> bool:
    result = await db.execute(select(Post).filter(Post.id == image_id))
    post = result.scalar_one_or_none()
    if post:
        await db.delete(post)
        await db.commit()
        return True
    return False
