import base64
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy.future import select

from users.models import User


def validate_image_file(image: UploadFile):
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")


async def read_image_contents(image: UploadFile) -> bytes:
    return await image.read()


def validate_image_size(contents: bytes):
    if len(contents) > 5 * 1024 * 1024:  # 5 MB
        raise HTTPException(status_code=400, detail="Image too large")


def convert_image_to_base64(image: UploadFile, contents: bytes) -> str:
    base64_str = base64.b64encode(contents).decode('utf-8')
    mime_type = image.content_type or 'image/png'
    return f"data:{mime_type};base64,{base64_str}"


async def get_user_by_id(db, user_id: UUID) -> User:
    query = select(User).where(user_id == User.id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user_profile_image(db, user: User, image_url: str):
    user.profile_image = image_url
    db.add(user)
    await db.commit()
    await db.refresh(user)
