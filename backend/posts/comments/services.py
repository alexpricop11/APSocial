from fastapi import HTTPException
from sqlalchemy import delete, update
from sqlalchemy.future import select

from database.database import AsyncSession
from posts.comments.models import Comment
from posts.comments.schemas import CreateComment, EditComment


class CommentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(self, comment: CreateComment):
        new_comment = Comment(
            **comment.dict()
        )
        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)
        if new_comment:
            return {"message": 'The comment created successfully'}
        return HTTPException(status_code=400, detail="Error created comment")

    async def get_comment_by_post_id(self, post_id):
        query = select(Comment).where(post_id == Comment.post_id)
        result = await self.db.execute(query)
        comments = result.scalars().all()
        if not comments:
            raise HTTPException(status_code=404, detail="No comments for this posts")
        return {
            'comments': comments,
            "num_comments": len(comments)
        }

    async def delete_comment(self, comment_id: int):
        query = select(Comment).where(comment_id == Comment.id)
        result = await self.db.execute(query)
        comment = result.scalar_one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        delete_query = delete(Comment).where(comment_id == Comment.id)
        await self.db.execute(delete_query)
        await self.db.commit()
        return {"message": "Comment deleted successfully"}

    async def edit_comment(self, comment_id: int, edit_comment: EditComment):
        query = select(Comment).where(comment_id == Comment.id)
        result = await self.db.execute(query)
        comment = result.scalar_one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        update_query = (
            update(Comment)
            .where(comment_id == Comment.id)
            .values(**edit_comment.dict(exclude_unset=True))
        )
        await self.db.execute(update_query)
        await self.db.commit()
        await self.db.refresh(comment)
        return {"message": "Comment updated successfully", "comment": comment}
