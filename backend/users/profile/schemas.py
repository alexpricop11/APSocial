from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserProfile(BaseModel):
    id: UUID
    username: str
    profile_image: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{9,15}$")
    birthday: Optional[date]

    class Config:
        from_attributes = True


class EditProfile(BaseModel):
    username: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    birthday: Optional[date]
