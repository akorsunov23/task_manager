from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException

from src.assign_tasks.models import TaskUser
from src.assign_tasks.repository import AssignTaskRepository
from src.assign_tasks.schemas import AssignTaskCreateSchema
from src.auth.models import User
from src.celery_tasks.tasks import send_email
from src.core import config


class AssignTaskService:
    """Сервис назначения задач."""

    def __init__(self, task_repo: AssignTaskRepository):
        self._task_repo: AssignTaskRepository = task_repo()

    async def create_all(
        self,
        user: User,
        data: AssignTaskCreateSchema
    ) -> None:
        """Массовое добавление объектов."""
        objects: list = []
        for user_id in data.users_id:
            objects.append(
                TaskUser(
                    end_datetime=data.end_datetime.date(),
                    appointed_id=user.id,
                    executor_id=user_id,
                    task_id=data.task_id,
                )
            )
        await self._task_repo.create_all(obj=objects)

    async def get_tasks_all(self, data: dict) -> list:
        """Получение всех задач."""
        return await self._task_repo.find_all(data=data)

    async def get_task_one(self, data: dict):
        """Получение объекта назначенной задачи."""
        return await self._task_repo.get_one(data=data)

    async def update_assign_task(self, assign_task_id: int, user_id: int):
        """Обновление записи назначения задачи."""
        obj = await self.get_task_one(
            data={"id": assign_task_id, "executor_id": user_id}
        )
        if obj:
            data = {
                "execution_status": True,
                "execution_datetime": datetime.utcnow()
            }
            return await self._task_repo.update_one(obj=obj, data=data)
        raise HTTPException(status_code=404, detail="Задача не найдена.")


class SendEmailService:
    """Сервис отправки сообщений."""

    def __init__(self):
        self._user = config.SMTP_USERNAME

    async def _message_generation(self, subject, msg):
        """Формирование сообщения."""
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = self._user
        message.attach(MIMEText(msg))
        message = message.as_string().encode("utf-8")

        return message

    async def msg_assign_task(
        self,
        user: User,
        e_mails: list,
        end_datetime:
        datetime,
        description: str
    ):
        """Отправка сообщения пользователю о назначении задачи."""
        for e_mail in e_mails:
            subject = f"Задача от {user.username}."
            message = (
                f"\n\nВам назначена задача:\n"
                f"Описание: {description}\n"
                f"Выполнить до: {end_datetime.date()}"
            )

            message = await self._message_generation(
                subject=subject,
                msg=message
            )
            send_email.delay(
                e_mail=e_mail,
                msg=message,
            )

    async def msg_overdue_task(self, data: list):
        """Отправка сообщения пользователю о просроченной задаче."""
        for e_mail, start_datetime in data:
            subject = "Просроченная задача."
            message = (f"\n\n У Вас просроченная "
                       f"задача от {start_datetime.date()}")

            message = await self._message_generation(
                subject=subject,
                msg=message
            )
            send_email.delay(
                e_mail=e_mail,
                msg=message,
            )
