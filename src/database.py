from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings
import redis.asyncio as redis

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_redis():
    return await redis.from_url(settings.REDIS_URL, decode_responses=True)



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

