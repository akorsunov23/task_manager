from datetime import date, timedelta

from src.assign_tasks.dependencies import assign_task_service
from src.assign_tasks.dependencies import service_send_email


async def get_overdue_tasks():
    """Получение данных пользователей с просроченными задачами ."""

    yesterday = date.today() - timedelta(days=1)
    data_filter: dict = {'execution_status': False, 'end_datetime': yesterday}
    overdue_tasks = await assign_task_service().get_tasks_all(data=data_filter)
    email_users: list = [(obj.executor.email, obj.start_datetime) for obj in overdue_tasks]
    print(email_users)
    await service_send_email().msg_overdue_task(data=email_users)
