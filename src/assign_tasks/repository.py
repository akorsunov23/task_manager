from src.assign_tasks.models import TaskUser
from src.utils.repository import SQLAlchemyRepository


class AssignTaskRepository(SQLAlchemyRepository):
    """Репозиторий над назначениями задач. """

    model = TaskUser
