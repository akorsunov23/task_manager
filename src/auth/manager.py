from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.core.config import AUTH_JWT_MANAGER_SECRET
from src.core.database import get_user_db
from .models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = AUTH_JWT_MANAGER_SECRET
    verification_token_secret = AUTH_JWT_MANAGER_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"Пользователь {user.id} зарегистрировался.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
