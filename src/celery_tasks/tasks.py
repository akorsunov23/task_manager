import asyncio
import smtplib

from src.celery_tasks.config import celery
from src.core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD
)


@celery.task
def send_email(e_mail: str, msg: str) -> bool:
    """Отправка сообщения в фоновом режиме"""
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(from_addr=SMTP_USERNAME, to_addrs=e_mail, msg=msg)
    return True


@celery.task
def scheduler_run():
    """Запуск рассылки о просроченных задачах."""
    from src.assign_tasks.utils import get_overdue_tasks

    loop = asyncio.get_event_loop()
    loop.create_task(get_overdue_tasks())
    loop.run_forever()
