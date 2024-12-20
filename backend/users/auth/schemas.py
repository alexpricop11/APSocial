from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class RegisterUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username must be at least 3 characters.")
    password: str = Field(..., min_length=6, max_length=100, description="Password must be at least 6 characters.")
    email: Optional[EmailStr] = Field(None, description="A valid email address.")
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{9,15}$",
                                        description="Phone number must include country code.")
    birthday: Optional[date] = Field(None, description="Date of birth in YYYY-MM-DD format.")


class LoginUser(BaseModel):
    username: str
    password: str = Field(..., min_length=6)
