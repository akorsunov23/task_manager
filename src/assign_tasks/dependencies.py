from src.assign_tasks.repository import AssignTaskRepository
from src.assign_tasks.services import AssignTaskService, SendEmailService


def assign_task_service():
    """Зависимость сервиса назначения задач."""

    return AssignTaskService(AssignTaskRepository)


def service_send_email():
    """Зависимость сервиса отправки сообщений."""

    return SendEmailService()
