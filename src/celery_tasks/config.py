from celery import Celery
from celery.schedules import crontab
from src.core import config

HOUR, MINUTE = tuple(map(int, config.NOTICE_TIME.split(":")))

celery = Celery(
    "celery_tasks",
    broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
    include=["src.celery_tasks.tasks"],
)

celery.conf.beat_schedule = {
    "everyday-task": {
        "task": "src.celery_tasks.tasks.scheduler_run",
        "schedule": crontab(hour=HOUR - 3, minute=MINUTE),
    }
}
