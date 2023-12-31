from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.assign_tasks import schemas
from src.assign_tasks.dependencies import (
    assign_task_service,
    service_send_email
)
from src.assign_tasks.services import AssignTaskService, SendEmailService
from src.auth.dependencies import user_service
from src.auth.models import User
from src.auth.routers import current_user
from src.auth.services import UserService
from src.tasks.dependencies import task_service
from src.tasks.services import TaskService

assign_task_app = APIRouter(
    tags=["Assignment of tasks"],
    prefix="/assign_task"
)


@assign_task_app.post(
    "/create",
    response_model=schemas.ResponseAssignTaskSchema
)
async def assign_task_users(
    data: schemas.AssignTaskCreateSchema,
    assign_task_serv: Annotated[
        AssignTaskService,
        Depends(assign_task_service)
    ],
    task_serv: Annotated[TaskService, Depends(task_service)],
    user_serv: Annotated[UserService, Depends(user_service)],
    email_serv: Annotated[SendEmailService, Depends(service_send_email)],
    user: User = Depends(current_user),
) -> schemas.ResponseAssignTaskSchema:
    """Назначение задачи пользователям."""
    try:
        task = await task_serv.get_one_task(
            data={"id": data.task_id, "owner_id": user.id}
        )
        if task:
            await assign_task_serv.create_all(user=user, data=data)
            users_email = await user_serv.get_users_email(
                users_id=data.users_id
            )
            await email_serv.msg_assign_task(
                user=user,
                e_mails=users_email,
                end_datetime=data.end_datetime,
                description=task.description,
            )
            return schemas.ResponseAssignTaskSchema(msg="Задача назначена.")
        raise HTTPException(
            status_code=404,
            detail="Задача не является вашей или данные не верные."
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Данные не верны.")


@assign_task_app.get("/get_tasks")
async def assign_task_users_get(
    assign_task_serv: Annotated[
        AssignTaskService,
        Depends(assign_task_service)
    ],
    user: User = Depends(current_user),
) -> List[schemas.AssignTaskSchema]:
    """Получение своих задач."""
    tasks = await assign_task_serv.get_tasks_all(data={"executor": user})
    if len(tasks) > 0:
        return tasks
    raise HTTPException(status_code=404, detail="Задач не найдено")


@assign_task_app.patch(
    "/update_task",
    response_model=schemas.ResponseAssignTaskSchema
)
async def assign_task_user_update(
    assign_task_id: int,
    assign_task_serv: Annotated[
        AssignTaskService,
        Depends(assign_task_service)
    ],
    user: User = Depends(current_user),
) -> schemas.ResponseAssignTaskSchema:
    """Обновление поставленной задачи."""
    await assign_task_serv.update_assign_task(
        assign_task_id=assign_task_id, user_id=user.id
    )
    return schemas.ResponseAssignTaskSchema(msg="Задача успешно выполнена.")
