from src.tasks.models import Task
from src.utils.repository import SQLAlchemyRepository


class AssignTaskRepository(SQLAlchemyRepository):
    """Репозиторий над назначениями задач. """

    model = Task
