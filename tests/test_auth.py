from sqlalchemy import select

from httpx import AsyncClient
from conftest import async_session_maker_test
from src.auth.models import User

COOKIE: dict = {}


async def test_register_user_success(client: AsyncClient):
    """Тестирование регистрации пользователя."""
    response = await client.post(
        "auth/register",
        json={
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "user_type": "user",
            "username": "string",
        },
    )

    assert response.status_code == 201


async def test_create_user_to_database(client: AsyncClient):
    """Тест на добавленную запись в БД."""
    async with async_session_maker_test() as session:
        query = select(User)
        result = await session.scalar(query)

        assert result.email == "user@example.com"
        assert result.username == "string"


async def test_register_user_not_success(client: AsyncClient):
    """Тестирование регистрации пользователя с неверными данными."""
    response = await client.post(
        "auth/register",
        json={
            "email": "user.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "user_type": "",
            "username": "string",
        },
    )

    assert response.status_code == 422


async def test_login_user_not_success(client: AsyncClient):
    """Тестирование аутентификации пользователя c неверными данными."""
    response = await client.post(
        "auth/jwt/login",
        data={
            "username": "user@examp.com",
            "password": "string",
        },
    )

    assert len(response.cookies) == 0


async def test_login_user_success(client: AsyncClient):
    """Тестирование аутентификации пользователя."""
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


async def test_info_me_user_success(client: AsyncClient):
    """Тестирование получения информации о себе."""
    response = await client.get("auth/users/me", cookies=COOKIE)

    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


async def test_update_data_user_success(client: AsyncClient):
    """Тестирование обновления данных пользователя."""
    response = await client.patch(
        "auth/users/me", json={"username": "new_user"}, cookies=COOKIE
    )

    assert response.status_code == 200


async def test_update_user_to_database(client: AsyncClient):
    """Тест на обновление пользователя в БД."""
    async with async_session_maker_test() as session:
        query = select(User)
        result = await session.scalar(query)

        assert result.username == "new_user"


async def test_logout_user_success(client: AsyncClient):
    """Тестирование выхода пользователя из системы."""
    response = await client.post("auth/jwt/logout", cookies=COOKIE)

    assert response.status_code == 204
    assert len(response.cookies) == 0
