from src.tasks.repository import TaskRepository
from src.tasks.services import TaskService


def task_service():
    """Зависимость сервиса задач."""

    return TaskService(TaskRepository)
