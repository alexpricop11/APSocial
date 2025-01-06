from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base


class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
                         primary_key=True)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
                          primary_key=True)

    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="followers"
    )
    following = relationship(
        "User", foreign_keys=[following_id], back_populates="following"
    )
