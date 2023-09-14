import asyncio

import aioschedule

from src.assign_tasks.utils import get_overdue_tasks


async def schedule():
    """Планировщик задач. Запускает функция в заданное время."""

    aioschedule.every().day.at('09:00').do(job_func=get_overdue_tasks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def startup_schedule():
    """Запуск планировщика."""

    asyncio.create_task(schedule())
