from pydantic import BaseModel
from uuid import UUID


class FollowRequest(BaseModel):
    user_id: UUID
