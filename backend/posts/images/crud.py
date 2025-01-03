import shutil
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from posts.images.models import Post
from posts.images.schemas import PostCreate


async def create_posts(db: AsyncSession, image: PostCreate) -> Post:
    file_location = f"posts/{uuid4()}.jpg"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(image.image.file, buffer)
    post = Post(image=file_location, user=image.user_id, uploaded_at=image.uploaded_at)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_posts(user_id: UUID) -> list[Post]:
    raise select(Post).filter(user_id == Post.user)


async def delete_image(db: AsyncSession, image_id: int):
    image = select(Post).filter(image_id == Post.id)
    if image:
        await db.delete(image)
        await db.commit()
        return True
    return False
