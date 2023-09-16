from httpx import AsyncClient
from sqlalchemy import select

from conftest import async_session_maker_test
from src.assign_tasks.models import TaskUser
from src.auth.models import User
from src.tasks.models import Task

COOKIE: dict = {}
ID_TASK: int = 0
ID_USER: int = 0
ID_ASSIGN_TASK: int = 0


async def test_login_user_for_test_assign_task_success(client: AsyncClient):
    """Аутентификация пользователя и получение его ID для дальнейших тестов."""
    response = await client.post(
        "auth/jwt/login",
        data={
            "username": "user@example.com",
            "password": "string",
        },
    )

    assert response.status_code == 204
    assert len(response.cookies) == 1

    global COOKIE
    COOKIE = {"fastapiusersauth": response.cookies.get("fastapiusersauth")}

    async with async_session_maker_test() as session:
        query = select(User).filter_by(email="user@example.com")
        result = await session.scalar(query)
        if result:
            global ID_USER
            ID_USER = result.id


async def test_task_create_for_test_assign_task_success(client: AsyncClient):
    """Тестирование создания задачи и получение её ID для дальнейших тестов."""
    response = await client.post(
        "task/create",
        json={
            "title": "string",
            "description": "string"
        },
        cookies=COOKIE
    )
    assert response.status_code == 200

    async with async_session_maker_test() as session:
        query = select(Task)
        result = await session.scalar(query)
        global ID_TASK
        ID_TASK = result.id


async def test_assign_task_success(client: AsyncClient):
    """Тест на назначение задачи."""
    response = await client.post(
        "assign_task/create",
        json={
            "users_id": [
                ID_USER,
            ],
            "task_id": ID_TASK,
            "end_datetime": "2023-09-16T10:58:39.579Z",
        },
        cookies=COOKIE,
    )
    assert response.status_code == 200


async def test_assign_task_not_success(client: AsyncClient):
    """Тест на назначение задачи c неверными данными."""
    response = await client.post(
        "assign_task/create",
        json={
            "users_id": [
                ID_USER - 1,
            ],
            "task_id": ID_TASK - 1,
            "end_datetime": "2023-09-16T10:58:39.579Z",
        },
        cookies=COOKIE,
    )
    assert response.status_code == 404


async def test_create_assign_task_to_database():
    """Тестирование на присутствие записи в БД."""
    async with async_session_maker_test() as session:
        query = select(TaskUser).filter_by(executor_id=ID_USER)
        result = await session.scalar(query)
        global ID_ASSIGN_TASK
        ID_ASSIGN_TASK = result.id
        assert result.task_id == ID_TASK


async def test_get_assign_task(client: AsyncClient):
    """Тестирование получение своих полученных задач."""
    response = await client.get("assign_task/get_tasks", cookies=COOKIE)

    assert response.status_code == 200
    assert "execution_status" in response.json()[0]
    assert isinstance(response.json(), list)


async def test_update_assign_task_success(client: AsyncClient):
    """Тестирование обновления полученной задачи."""
    response = await client.patch(
        "assign_task/update_task",
        params={"assign_task_id": ID_ASSIGN_TASK},
        cookies=COOKIE,
    )

    assert response.status_code == 200


async def test_update_assign_task_to_database():
    """Тестирование на обновление записи в БД."""
    async with async_session_maker_test() as session:
        query = select(TaskUser).filter_by(id=ID_ASSIGN_TASK)
        result = await session.scalar(query)

        assert result.execution_status is True
        assert result.execution_datetime is not None
