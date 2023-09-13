from fastapi import APIRouter, Depends
from src.assign_tasks import schemas
from src.auth.models import User
from src.auth.routers import current_superuser

assign_task_app = APIRouter(
    tags=["Assignment of tasks"],
    prefix="/assign_task"
)


@assign_task_app.post('/create')
async def assign_task_users(
    data: schemas.AssignTaskCreateSchema,
    # task_serv: Annotated[TaskService, Depends(task_service)],
    user: User = Depends(current_superuser),
):
    """Назначение задачи пользователям."""
    print(data.users_id)
    pass