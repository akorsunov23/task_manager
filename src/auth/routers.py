from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate, UserUpdate

auth_app = APIRouter(tags=["CRUD User"], prefix="/auth")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)

auth_app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)
auth_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

auth_app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)
