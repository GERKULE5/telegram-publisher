import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .models import Base

database_url = os.getenv('DATABASE_URL')
print(database_url)
engine = create_async_engine(database_url)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


def async_connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as conn:
            return await func(conn, *args, **kwargs)

    return wrapper


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)