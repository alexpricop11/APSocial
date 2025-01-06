# from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
# from sqlalchemy.dialects.postgresql import UUID
# from database.database import Base
#
#
# class Like(Base):
#     __tablename__ = 'Likes'
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
#     user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
#     target_type = Column(String, nullable=False)
#     target_id = Column(Integer, nullable=False)
#     is_like = Column(Boolean, nullable=False, default=False)
#     created_at = Column(DateTime, nullable=False)
