from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Date, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base
from follow.models import Follow
from posts.posts.models import post_likes


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    profile_image = Column(Text, nullable=True)
    password = Column(String(512), nullable=False)
    email = Column(String(255), nullable=True, unique=False)
    phone_number = Column(String(20), nullable=True)
    birthday = Column(Date, nullable=True)
    bio = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="user")
    liked_posts = relationship(
        "Post", secondary=post_likes, back_populates="liked_by_users"
    )

    followers = relationship(
        "Follow", foreign_keys=[Follow.following_id], back_populates="following"
    )
    following = relationship(
        "Follow", foreign_keys=[Follow.follower_id], back_populates="follower"
    )
    posts_count = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
