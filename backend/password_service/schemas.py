from pydantic import BaseModel, Field, EmailStr


class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100, description="Password must be at least 6 characters.")


class ResetPassword(BaseModel):
    email: EmailStr


class ResetPasswordConfirm(BaseModel):
    email: EmailStr
    reset_code: str
    new_password: str = Field(..., min_length=6, max_length=100, description="Password must be at least 6 characters.")
