from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base


class Post(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    user = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    image = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)
    comments = relationship("Comment", back_populates="post")
