from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
AsyncSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSession() as session:
        yield session


Base = declarative_base()
