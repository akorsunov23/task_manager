import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from src.assign_tasks.models import TaskUser
from src.auth.models import User
from src.core.config import async_db_engine_settings_test
from src.core.database import get_async_session
from src.main import app
from src.tasks.models import Task

engine_test = create_async_engine(async_db_engine_settings_test)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    """Сессия тестовой базы данных."""
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = get_async_session_test


@pytest.fixture(autouse=True, scope="session")
async def run_database():
    """Отчистка БД после проведения тестов."""
    yield
    async with async_session_maker() as session:
        user_base = select(User)
        result_user = await session.scalar(user_base)
        if result_user:
            await session.delete(result_user)
            await session.commit()

        task_base = select(Task)
        result_task = await session.scalar(task_base)
        if result_task:
            await session.delete(result_task)
            await session.commit()

        task_user_base = select(TaskUser)
        result_task_user = await session.scalar(task_user_base)
        if result_task_user:
            await session.delete(result_task_user)
            await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Получение асинхронного клиента."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
