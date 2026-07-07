from contextlib import contextmanager
from decouple import config

from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

engine = create_async_engine(config('DATABASE_URL'), future=True)
SessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with SessionLocal() as session:
        yield session


celery_engine = create_async_engine(
    config('DATABASE_URL'),
    poolclass=NullPool,
)
AsyncCelerySession = async_sessionmaker(celery_engine, expire_on_commit=False)

