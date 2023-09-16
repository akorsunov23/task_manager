from datetime import datetime

from pydantic import BaseModel
from src.auth.schemas import UserSchema


class TaskSchema(BaseModel):
    """Схема модели задач."""

    id: int
    title: str
    description: str
    created_on: datetime
    updated_on: datetime
    owner: UserSchema


class TaskCreateSchema(BaseModel):
    """Схема добавления задачи."""

    title: str
    description: str


class TaskUpdateSchema(BaseModel):
    """Схема обновление задачи."""

    id: int
    title: str
    description: str


class ResponseTaskSchema(BaseModel):
    """Схема успешного ответа на запросы."""

    msg: str
