from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.repository import UserRepository
from src.core.database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Получение текущего пользователя."""
    yield SQLAlchemyUserDatabase(session, User)


class UserService:
    """Сервис пользователей."""

    def __init__(self, user_repo: UserRepository):
        self._user_repo: UserRepository = user_repo()

    async def get_users_email(self, users_id: list) -> list:
        """Получение списка пользовательской почты."""
        users_email: list = []
        for user_id in users_id:
            user = await self._user_repo.get_one(data={"id": user_id})
            users_email.append(user.email)
        return users_email
