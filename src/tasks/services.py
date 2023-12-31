from src.tasks.repository import TaskRepository


class TaskService:
    """Сервис задач."""

    def __init__(self, task_repo: TaskRepository):
        self._task_repo: TaskRepository = task_repo()

    async def get_all_task(self, data: dict):
        """Получение всех задач."""
        tasks = await self._task_repo.find_all(data=data)
        return tasks

    async def get_one_task(self, data: dict):
        """Получение одной задачи."""
        task = await self._task_repo.get_one(data=data)
        return task

    async def delete_task(self, obj):
        """
        Удаление задачи.
        :param obj: Объект задачи.
        """
        await self._task_repo.delete_one(obj=obj)

    async def create_task(self, data: dict):
        """Добавление задачи."""
        return await self._task_repo.add_one(data=data)

    async def update_task(self, obj, data: dict):
        """Обновление задачи"""
        await self._task_repo.update_one(obj=obj, data=data)
