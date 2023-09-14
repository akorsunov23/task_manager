from src.auth.models import User
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Репозиторий пользователей."""

    model = User
