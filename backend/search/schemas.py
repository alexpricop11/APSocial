from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ResultSearch(BaseModel):
    id: UUID
    profile_image: Optional[str] = None
    username: str
