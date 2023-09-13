from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.assign_tasks import schemas
from src.assign_tasks.dependencies import assign_task_service
from src.assign_tasks.services import AssignTaskService
from src.auth.models import User
from src.auth.routers import current_user

assign_task_app = APIRouter(
    tags=["Assignment of tasks"],
    prefix="/assign_task"
)


@assign_task_app.post('/create')
async def assign_task_users(
    data: schemas.AssignTaskCreateSchema,
    assign_task_serv: Annotated[AssignTaskService, Depends(assign_task_service)],
    user: User = Depends(current_user),
):
    """Назначение задачи пользователям."""
    try:
        await assign_task_serv.create_all(
            user=user,
            data=data
        )
        return {'msg': "Задача назначены"}
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Данные не верны."
        )
