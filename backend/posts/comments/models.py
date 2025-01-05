from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base


class Comment(Base):
    __tablename__ = 'Comments'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    user = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    post_id = Column(ForeignKey('Posts.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

