from src.tasks.models import Task
from src.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    """Репозиторий над задачами. """

    model = Task
