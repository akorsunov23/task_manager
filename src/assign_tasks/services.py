from src.assign_tasks.models import TaskUser
from src.assign_tasks.repository import AssignTaskRepository
from src.assign_tasks.schemas import AssignTaskCreateSchema
from src.auth.models import User


class AssignTaskService:
    """Сервис назначения задач."""

    def __init__(self, task_repo: AssignTaskRepository):
        self._task_repo: AssignTaskRepository = task_repo()

    async def get_all_task(self):
        """Получение всех задач."""
        tasks = await self._task_repo.find_all()
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

    async def create_all(self, user: User, data: AssignTaskCreateSchema):
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
