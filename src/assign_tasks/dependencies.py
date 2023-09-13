from src.assign_tasks.repository import AssignTaskRepository
from src.assign_tasks.services import AssignTaskService


def assign_task_service():
    """Зависимость сервиса назначения задач."""

    return AssignTaskService(AssignTaskRepository)
