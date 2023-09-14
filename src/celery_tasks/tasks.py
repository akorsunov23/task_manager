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
