from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from fastapi import UploadFile


class PostBase(BaseModel):
    image_url: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, title="Upload Date",
                                  description="The date when the image was uploaded")


class PostCreate(PostBase):
    user_id: UUID = Field(..., title="User ID", description="The ID of the user uploading the image")
    image: UploadFile = Field(..., title="Image", description="The image file to upload")


class PostInDB(PostBase):
    id: int = Field(..., title="Image ID", description="Unique identifier of the image")
    user_id: UUID = Field(..., title="User ID", description="The ID of the user uploading the image")

    class Config:
        from_attributes = True
