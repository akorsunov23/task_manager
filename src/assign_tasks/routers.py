from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.assign_tasks import schemas
from src.assign_tasks.dependencies import assign_task_service, service_send_email
from src.assign_tasks.services import AssignTaskService, SendEmailService
from src.auth.models import User
from src.auth.routers import current_user
from src.tasks.dependencies import task_service
from src.tasks.services import TaskService

assign_task_app = APIRouter(
    tags=["Assignment of tasks"],
    prefix="/assign_task"
)


@assign_task_app.post('/create')
async def assign_task_users(
    data: schemas.AssignTaskCreateSchema,
    assign_task_serv: Annotated[AssignTaskService, Depends(assign_task_service)],
    task_serv: Annotated[TaskService, Depends(task_service)],
    email_serv: Annotated[SendEmailService, Depends(service_send_email)],
    user: User = Depends(current_user),
):
    """Назначение задачи пользователям."""
    try:
        await assign_task_serv.create_all(
            user=user,
            data=data
        )
        task = await task_serv.get_one_task(data={'id': data.task_id})
        await email_serv.msg_assign_task(
            user=user,
            e_mail='kors21vek@mail.ru',
            end_datetime=data.end_datetime,
            description=task.description
        )
        return {'msg': "Задача назначены"}
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Данные не верны."
        )
