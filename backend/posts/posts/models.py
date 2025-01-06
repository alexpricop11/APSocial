from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base

post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("post_id", UUID(as_uuid=True), ForeignKey("posts.id")),
)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, index=True)
    image = Column(String, nullable=False)
    content = Column(String, nullable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="posts")
    uploaded_at = Column(DateTime, nullable=False)
    comments = relationship("Comment", back_populates="post")
    liked_by_users = relationship(
        "User", secondary=post_likes, back_populates="liked_posts"
    )
