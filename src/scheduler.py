import asyncio

import aioschedule

from src.assign_tasks.utils import get_overdue_tasks
from src.core.config import NOTICE_TIME


async def schedule():
    """Планировщик задач. Запускает функция в заданное время."""

    aioschedule.every().day.at(NOTICE_TIME).do(job_func=get_overdue_tasks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def startup_schedule():
    """Запуск планировщика."""

    asyncio.create_task(schedule())
