from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.tasks.schemas import TaskSchema


class Task(Base):
    """Модель задачи."""

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    # Связь с таблицей пользователя
    owner = relationship("User", back_populates="task", lazy="selectin")
    # Связь с таблицей постановки задачи
    task_user = relationship(
        "TaskUser",
        back_populates="task",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"Task {self.id}: owner by - {self.owner}"

    def to_read_model(self):
        return TaskSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            created_on=self.created_on,
            updated_on=self.updated_on,
            owner=self.owner.to_read_model(),
        )
