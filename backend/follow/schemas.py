from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class FollowRequest(BaseModel):
    user_id: UUID


class FollowList(BaseModel):
    id: UUID
    username: str
    profile_image: Optional[str]

    class Config:
        from_attributes = True


class FollowersList(BaseModel):
    followers: list[FollowList]


class FollowingList(BaseModel):
    following: list[FollowList]
