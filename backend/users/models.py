from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Date, Text
from sqlalchemy.dialects.postgresql import UUID

from database.database import Base


class User(Base):
    __tablename__ = 'Users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    profile_image = Column(Text, nullable=True)
    password = Column(String(512), nullable=False)
    email = Column(String(255), nullable=True, unique=False)
    phone_number = Column(String(20), nullable=True)
    birthday = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

