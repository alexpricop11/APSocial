from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserProfile(BaseModel):
    id: UUID
    username: str
    profile_image: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{9,15}$")
    birthday: Optional[date] = None
    bio: Optional[str] = None
    followers_count: int
    following_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class OtherUserProfile(BaseModel):
    id: UUID
    username: str
    profile_image: Optional[str] = None
    birthday: Optional[date] = None
    bio: Optional[str] = None
    followers_count: int
    following_count: int
    created_at: datetime
    is_following: Optional[bool] = None

    class Config:
        from_attributes = True


class EditProfile(BaseModel):
    profile_image: Optional[str] = None
    username: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    birthday: Optional[date]
    bio: Optional[str]
