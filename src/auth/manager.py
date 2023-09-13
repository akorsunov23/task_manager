from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    schemas,
    models
)

from src.auth.models import User
from src.auth.schemas import UserTypeEnum
from src.auth.services import get_user_db
from src.core.config import AUTH_JWT_MANAGER_SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = AUTH_JWT_MANAGER_SECRET
    verification_token_secret = AUTH_JWT_MANAGER_SECRET

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Добавление пользователя в БД.

        :param user_create: Схема добавления пользователя.
        :param safe: Если True, конфиденциальные значения,
        такие как is_superuser или is_verified,
        будет игнорироваться во время создания,
        по умолчанию установлено значение False.
        :param request: Дополнительный запрос FastAPI, который
         запустил операцию, по умолчанию — None.
        :raises UserAlreadyExists: Если пользователь уже существует.
        :return: Новый пользователь.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["user_type"] = UserTypeEnum.USER

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
