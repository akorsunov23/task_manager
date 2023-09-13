from src.auth.repository import UserRepository
from src.auth.services import UserService


def user_service():
    """Зависимость сервиса задач."""

    return UserService(UserRepository)
