import smtplib

from src.celery_tasks.config import celery
from src.core.config import (
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD
)


@celery.task
def send_email(
        e_mail,
        msg,
) -> bool:
    """Отправка сообщения в фоновом режиме"""
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(
                from_addr=e_mail,
                to_addrs=SMTP_USERNAME,
                msg=msg
            )
        return True
    except Exception as ex:
        return False
