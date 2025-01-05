from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateComment(BaseModel):
    text: str


class EditComment(CreateComment):
    text: str


class CommentBase(CreateComment):
    id: int
    user: UUID
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True
