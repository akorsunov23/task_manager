from httpx import AsyncClient
from sqlalchemy import select

from conftest import async_session_maker_test
from src.tasks.models import Task

COOKIE: dict = {}
ID_TASK: int = 0


async def test_login_user_for_test_task_success(client: AsyncClient):
    """Аутентификация пользователя для дальнейших тестов."""
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


async def test_task_create_success(client: AsyncClient):
    """Тестирование создания задачи."""
    response = await client.post(
        "task/create",
        json={
            "title": "string",
            "description": "string"
        },
        cookies=COOKIE
    )
    assert response.status_code == 200


async def test_create_task_to_database(client: AsyncClient):
    """Тест на добавленную запись в БД."""
    async with async_session_maker_test() as session:
        query = select(Task)
        result = await session.scalar(query)
        global ID_TASK
        ID_TASK = result.id
        assert result.title == "string"


async def test_task_get_one_success(client: AsyncClient):
    """Тестирование получение добавленной задачи."""
    response = await client.get(
        "task/read_one", params={"task_id": ID_TASK}, cookies=COOKIE
    )

    assert response.status_code == 200
    assert response.json()["title"] == "string"


async def test_task_get_all_success(client: AsyncClient):
    """Тестирование получение всех добавленных задач."""
    response = await client.get("task/read_all", cookies=COOKIE)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "owner" in response.json()[0]


async def test_task_update_success(client: AsyncClient):
    """Тестирование обновление добавленной задачи."""
    response = await client.put(
        "task/update",
        json={
            "id": ID_TASK,
            "title": "new_title",
            "description": "new_description"
        },
        cookies=COOKIE,
    )

    assert response.status_code == 200


async def test_update_task_to_database(client: AsyncClient):
    """Тест на обновленную запись в БД."""
    async with async_session_maker_test() as session:
        query = select(Task).filter_by(id=ID_TASK)
        result = await session.scalar(query)

        assert result.title == "new_title"
        assert result.description == "new_description"


async def test_task_delete_not_success(client: AsyncClient):
    """Тестирование удаления добавленной задачи с неверными данными."""
    response = await client.delete(
        "task/delete",
        params={
            "id": ID_TASK - 1,
        },
        cookies=COOKIE,
    )

    assert response.status_code == 422


async def test_task_delete_success(client: AsyncClient):
    """Тестирование удаления добавленной задачи."""
    response = await client.delete(
        "task/delete",
        params={
            "task_id": ID_TASK,
        },
        cookies=COOKIE,
    )

    assert response.status_code == 200


async def test_empty_task_to_database(client: AsyncClient):
    """Тест на пустую БД."""
    async with async_session_maker_test() as session:
        query = select(Task).filter_by(id=ID_TASK)
        result = await session.scalar(query)

        assert result is None
