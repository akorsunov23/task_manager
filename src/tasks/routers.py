from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.auth.models import User
from src.auth.routers import current_user
from src.tasks import schemas
from src.tasks.dependencies import task_service
from src.tasks.services import TaskService

task_app = APIRouter(prefix="/task", tags=["CRUD Task"])


@task_app.post(
    "/create",
    response_model=schemas.ResponseTaskSchema
)
async def create_task(
    data: schemas.TaskCreateSchema,
    task_serv: Annotated[TaskService, Depends(task_service)],
    user: User = Depends(current_user),
) -> schemas.ResponseTaskSchema:
    """
    Добавление задачи в БД.
    :param data: Схема добавления задачи.
    :param task_serv: Сервис для работы с задачами.
    :param user: Текущий пользователь.
    """

    try:
        task = await task_serv.create_task(
            data={
                "title": data.title,
                "description": data.description,
                "owner_id": user.id,
            }
        )
        return schemas.ResponseTaskSchema(
            msg=f"Задача добавлена, ID:{task}"
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Задача с таким заголовком уже добавлена."
        )


@task_app.get(
    "/read_one",
    response_model=schemas.TaskSchema
)
async def read_task_one(
    task_id: int,
    task_serv: Annotated[TaskService, Depends(task_service)],
    user: User = Depends(current_user),
) -> schemas.TaskSchema:
    """
    Чтение одной задачи.
    :param task_id: ID задачи.
    :param task_serv: Сервис для работы с задачами.
    :param user: Текущий пользователь.
    """

    task = await task_serv.get_one_task(
        data={
            "id": task_id,
            "owner_id": user.id,
        }
    )
    if task:
        return task.to_read_model()
    raise HTTPException(status_code=404, detail="Задачи не существует")


@task_app.get("/read_all")
async def read_tasks_all(
    task_serv: Annotated[TaskService, Depends(task_service)],
    user: User = Depends(current_user),
) -> List[schemas.TaskSchema]:
    """
    Чтение всех доступных задач.
    :param task_serv: Сервис для работы с задачами.
    :param user: Текущий пользователь.
    """

    tasks = await task_serv.get_all_task(data={"owner_id": user.id})
    if len(tasks) > 0:
        return tasks
    raise HTTPException(status_code=404, detail="Задач не добавлено.")


@task_app.put(
    "/update",
    response_model=schemas.ResponseTaskSchema
)
async def update_task(
    data: schemas.TaskUpdateSchema,
    task_serv: Annotated[TaskService, Depends(task_service)],
    user: User = Depends(current_user),
) -> schemas.ResponseTaskSchema:
    """
    Обновление задачи.
    :param data: Данные для обновления задачи.
    :param task_serv: Сервис для работы с задачами.
    :param user: Текущий пользователь.
    """

    task = await task_serv.get_one_task(
        data={
            "id": data.id,
            "owner_id": user.id,
        }
    )
    if task:
        try:
            await task_serv.update_task(
                obj=task,
                data={
                    "title": data.title,
                    "description": data.description
                }
            )
            return schemas.ResponseTaskSchema(
                msg=f"Задача ID:{task.id} успешно обновлена"
            )
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Задача с таким заголовком уже добавлена."
            )
    raise HTTPException(status_code=404, detail="Задачи не существует")


@task_app.delete(
    "/delete",
    response_model=schemas.ResponseTaskSchema
)
async def delete_task(
    task_id: int,
    task_serv: Annotated[TaskService, Depends(task_service)],
    user: User = Depends(current_user),
) -> schemas.ResponseTaskSchema:
    """
    Удаление задачи.
    :param task_id: ID задачи для удаления.
    :param task_serv: Сервис для работы с задачами.
    :param user: Текущий пользователь.
    """
    task = await task_serv.get_one_task(
        data={
            "id": task_id,
            "owner_id": user.id,
        }
    )
    if task:
        await task_serv.delete_task(
            obj=task,
        )
        return schemas.ResponseTaskSchema(
            msg=f"Задача ID:{task.id} успешно удалена."
        )

    raise HTTPException(status_code=404, detail="Задачи не существует")
