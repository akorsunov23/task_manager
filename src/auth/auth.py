from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from src.core.config import AUTH_JWT_STRATEGY_SECRET

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    """Кодирование токена. Хранение токена настроена на 1 час. (3600)"""
    return JWTStrategy(secret=AUTH_JWT_STRATEGY_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
