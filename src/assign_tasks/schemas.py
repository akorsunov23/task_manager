from datetime import datetime
from typing import List

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


class AssignTaskCreateSchema(BaseModel):
    """Схема назначения задачи."""

    users_id: List[int]
    task_id: int
    end_date: datetime


class TaskUpdateSchema(BaseModel):
    """Схема обновление задачи."""

    id: int
    title: str
    description: str
