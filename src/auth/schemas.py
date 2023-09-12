import enum

from fastapi_users import schemas
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserTypeEnum(enum.Enum):
	"""Типы пользователя."""
	USER = 'user'
	ADMIN = 'admin'


class UserSchema(BaseModel):
	"""Схема модели пользователя."""
	id: int
	email: EmailStr
	user_type: UserTypeEnum
	username: str


class UserRead(schemas.BaseUser[int]):
	pass


class UserCreate(schemas.BaseUserCreate):
	pass


class UserUpdate(schemas.BaseUserUpdate):
	pass
