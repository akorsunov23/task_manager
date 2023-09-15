from httpx import AsyncClient


async def test_register_user_success(client: AsyncClient):
	"""Тестирование регистрации пользователя."""
	response = await client.post("auth/register", json={
			"email": "user@example.com",
			"password": "string",
			"is_active": True,
			"is_superuser": False,
			"is_verified": False,
			"user_type": "user",
			"username": "string"
		}
	)
	assert response.status_code == 201

#  TODO: написать тест на добавление в БД


async def test_register_user_not_success(client: AsyncClient):
	"""Тестирование регистрации пользователя с неверными данными."""
	response = await client.post("auth/register", json={
			"email": "user.com",
			"password": "string",
			"is_active": True,
			"is_superuser": False,
			"is_verified": False,
			"user_type": "",
			"username": "string"
		}
	)
	assert response.status_code == 422


async def test_login_user_success(client: AsyncClient):
	"""Тестирование регистрации пользователя."""
	response = await client.post("auth/jwt/login", headers={
			"username": "user@example.com",
			"password": "string",
		}
	)
	assert response.status_code == 201