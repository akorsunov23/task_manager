from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

from src.auth.schemas import UserSchema
from src.tasks.schemas import TaskSchema


class AssignTaskSchema(BaseModel):
    """Схема модели постановки задач."""
    id: int
    start_datetime: datetime
    end_datetime: datetime
    execution_datetime: Union[datetime, None]
    execution_status: bool
    appointed: UserSchema
    executor: UserSchema
    task: TaskSchema


class AssignTaskCreateSchema(BaseModel):
    """Схема назначения задачи."""
    users_id: List[int]
    task_id: int
    end_datetime: datetime


class ResponseAssignTaskSchema(BaseModel):
    """Схема успешного ответа на запросы."""
    msg: str
