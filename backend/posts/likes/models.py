from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database import Base


class Like(Base):
    __tablename__ = 'Likes'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    target_type = Column(String, nullable=False)
    target_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    post = relationship("Post", primaryjoin="and_(Like.target_id==Post.id, Like.target_type=='Post')")
    comment = relationship("Comment", primaryjoin="and_(Like.target_id==Comment.id, Like.target_type=='Comment')")
