import asyncio

from passlib.context import CryptContext
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.auth.models import User
from src.auth.schemas import UserTypeEnum
from src.core import config
from src.core.database import async_session_maker


async def createsuperuser():
    """
    Добавление суперпользователя через терминал.
    Добавить в .env данные суперпользователя.
    Запустить в терминале 'python createsuperuser.py'.
    """
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        admin_data: dict = {
            "email": config.ADMIN_EMAIL,
            "hashed_password": context.hash(config.ADMIN_PASSWORD),
            "username": config.ADMIN_USERNAME,
            "user_type": UserTypeEnum.ADMIN,
            "is_active": True,
            "is_superuser": True,
            "is_verified": True,
        }
        async with async_session_maker() as session:
            stmt = insert(User).values(**admin_data)
            await session.execute(stmt)
            await session.commit()
        print("Суперпользователь добавлен.")
    except IntegrityError:
        print("Суперпользователь с такими данными уже существует.")


if __name__ == "__main__":
    asyncio.run(createsuperuser())
