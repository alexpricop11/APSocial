# from uuid import UUID
# from datetime import datetime
# from posts.likes.schemas import LikeCreate
# from posts.likes.repository import LikeRepository
#
#
# class LikeService:
#     def __init__(self, like_repository: LikeRepository):
#         self.like_repository = like_repository
#
#     async def toggle_like(self, user_id: UUID, target_type: str, target_id: int):
#         existing_like = await self.like_repository.get_like_target(user_id, target_type, target_id)
#         if existing_like:
#             await self.like_repository.delete_like(existing_like)
#             return None
#         new_like = LikeCreate(
#             user_id=user_id,
#             target_type=target_type,
#             target_id=target_id,
#             is_like=True,
#             created_at=datetime.now()
#         )
#         return await self.like_repository.create_like(new_like)
