import enum
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserTypeEnum(enum.Enum):
    """Типы пользователя."""

    USER = "user"
    ADMIN = "admin"


class UserSchema(BaseModel):
    """Схема модели пользователя."""

    id: int
    email: EmailStr
    user_type: UserTypeEnum
    username: str


class UserRead(schemas.BaseUser[int]):
    """Схема чтения пользователя."""

    id: int
    user_type: UserTypeEnum
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    """Схема добавления пользователя."""

    user_type: UserTypeEnum = UserTypeEnum.USER
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления пользователя."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
