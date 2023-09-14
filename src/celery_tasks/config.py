from celery import Celery

from src.core import config

celery = Celery(
    'celery_tasks',
    broker=f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}',
)
