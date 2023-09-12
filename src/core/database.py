from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from .config import async_db_engine_settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(async_db_engine_settings)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Сессия базы данных."""
    async with async_session_maker() as session:
        yield session
