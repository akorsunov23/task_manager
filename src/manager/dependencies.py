from src.manager.repository import TaskRepository
from src.manager.services import TaskService


def task_service():
    """Зависимость сервиса задач."""

    return TaskService(TaskRepository)
