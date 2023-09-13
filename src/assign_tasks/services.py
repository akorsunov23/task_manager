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

    async def create_all(self, user: User, data: AssignTaskCreateSchema) -> None:
        """Массовое добавление объектов."""
        objects: list = []
        for user_id in data.users_id:
            objects.append(
                TaskUser(
                    end_datetime=data.end_datetime.date(),
                    appointed_id=user.id,
                    executor_id=user_id,
                    task_id=data.task_id
                )
            )
        await self._task_repo.create_all(objects=objects)

    async def get_tasks_all(self, data: dict) -> list:
        """Получение всех задач."""
        return await self._task_repo.find_all(data=data)

    async def get_task_one(self, data: dict):
        """Получение объекта назначенной задачи."""
        return await self._task_repo.get_one(data=data)

    async def update_assign_task(self, assign_task_id: int, user_id: int):
        """Обновление записи назначения задачи."""
        obj = await self.get_task_one(
            data={
                'id': assign_task_id,
                'executor_id': user_id
            }
        )
        if obj:
            data = {
                'execution_status': True,
                'execution_datetime': datetime.utcnow()
            }
            return await self._task_repo.update_one(obj=obj, data=data)
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена."
        )


class SendEmailService:
    """Сервис отправки сообщений."""
    def __init__(self):
        self._user = config.SMTP_USERNAME

    async def _message_generation(self, subject, msg):
        """Формирование сообщения. """
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self._user
        message.attach(MIMEText(msg))
        message = message.as_string().encode('utf-8')

        return message

    async def msg_assign_task(
            self,
            user: User,
            e_mails: list,
            end_datetime: datetime,
            description: str
    ):
        """Отправка сообщения пользователю о назначении задачи."""
        for e_mail in e_mails:
            subject = f'Задача от {user.username}.'
            message = (
                f'\n\nВам назначена задача:\n'
                f'Описание: {description}\n'
                f'Выполнить до: {end_datetime.date()}'
            )

            message = await self._message_generation(
                subject=subject,
                msg=message
            )
            send_email.delay(
                e_mail=e_mail,
                msg=message,
            )

    async def msg_submit(self, client):
        """Отправка сообщений 'оставить заявку'."""
        # тема сообщения администратору
        subject = 'Новая заявка от <ELEMINT>'
        # тема сообщения клиенты
        subject_response = 'Спасибо за обращение в <ELEMINT>'
        # сообщение администратору
        message_text = f'\n\nПолучена заявка от: \n\n' \
                       f'Имя: {client.first_name}\n' \
                       f'Фамилия: {client.last_name}\n' \
                       f'E-mail: {client.e_mail}\n'
        # ответ клиенту
        message_response = f'{client.first_name} Ваш запрос отправлен. '\
                           f'Спасибо. ' \
                           f'\n\nМы свяжемся с вами в самое ближайшее время.'

        if client.phone_number:
            message_text += f'Номер телефона: {client.phone_number}\n'
        if client.name_organization:
            message_text += f'Организация: {client.name_organization}\n'
        if client.TIN:
            message_text += f'ИНН: {client.TIN}\n'

        subject_list = [subject, subject_response, ]
        msg_list = [message_text, message_response, ]

        message, message_client = await self._message_generation(
            e_mail=client.e_mail,
            subject=subject_list,
            msg=msg_list
        )
        return send_email.delay(
            e_mail=client.e_mail,
            msg=message,
            msg_client=message_client
        )
