from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from posts.comments.schemas import CreateComment, EditComment
from posts.comments.services import CommentService

from users.auth.jwt import get_current_user
from users.models import User

comment = APIRouter(tags=['comments'])


@comment.post('/create-comment')
async def create_comments(
        create: CreateComment,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    service = CommentService(db)
    return await service.create_comment(create, current_user.id, create.post_id)


@comment.get('/get-comments')
async def get_comments(
        post_id: int,
        db: AsyncSession = Depends(get_db)
):
    comment_service = CommentService(db)
    return await comment_service.get_comment_by_post_id(post_id)


@comment.delete('/delete-comment')
async def delete_comment(
        post_id: int,
        db: AsyncSession = Depends(get_db),
):
    delete_service = CommentService(db)
    return await delete_service.delete_comment(post_id)


@comment.put('/edit-comment')
async def edit_comments(
        comment_id: int,
        edit_comment: EditComment,
        db: AsyncSession = Depends(get_db)
):
    service = CommentService(db)
    return await service.edit_comment(comment_id, edit_comment)
