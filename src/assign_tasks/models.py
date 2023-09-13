from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.assign_tasks.schemas import AssignTaskSchema


class TaskUser(Base):
    """Модель назначенных задач."""

    __tablename__ = "task_user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    start_datetime = Column(DateTime, default=datetime.utcnow)
    end_datetime = Column(DateTime, nullable=False)
    execution_datetime = Column(DateTime, nullable=True)
    execution_status = Column(Boolean, default=False, nullable=False)
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    appointed_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    executor_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    # Связь с таблицей пользователя
    appointed = relationship(
        "User",
        back_populates="appointed_task",
        lazy="selectin",
        foreign_keys="TaskUser.appointed_id"
    )
    executor = relationship(
        "User",
        back_populates="executor_task",
        lazy="selectin",
        foreign_keys="TaskUser.executor_id"
    )

    # Связь с таблицей задач
    task = relationship("Task", back_populates="task_user", lazy="selectin")

    def __repr__(self) -> str:
        # return f"Task assigned from {self.appointed} to {self.executor}"
        return f"Task assigned from"

    def to_read_model(self):
        return AssignTaskSchema(
            id=self.id,
            start_datetime=self.start_datetime,
            end_datetime=self.end_datetime,
            execution_datetime=self.execution_datetime,
            execution_status=self.execution_status,
            appointed=self.appointed.to_read_model(),
            executor=self.executor.to_read_model(),
            task=self.task.to_read_model()
        )
