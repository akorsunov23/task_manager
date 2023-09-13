from datetime import datetime

from pydantic import BaseModel


class TaskSchema(BaseModel):
    """Схема задач."""
    id: int
    title: str
    description: str
    created_on: datetime
    updated_on: datetime
    owner: str
