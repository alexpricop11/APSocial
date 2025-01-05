from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateComment(BaseModel):
    user: UUID
    post_id: int
    text: str
    created_at: datetime


class EditComment(CreateComment):
    pass


class CommentBase(CreateComment):
    id: int

    class Config:
        from_attributes = True
