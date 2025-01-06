# from datetime import datetime
# from uuid import UUID
# from pydantic import BaseModel, Field
#
#
# class LikeBase(BaseModel):
#     user_id: UUID
#     target_type: str
#     target_id: int
#     is_like: bool = Field(default=False)
#     created_at: datetime
#
#
# class LikeCreate(LikeBase):
#     pass
#
#
# class LikeSchema(LikeBase):
#     id: int
#
#     class Config:
#         from_attributes = True
