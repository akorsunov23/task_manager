"""Получение данных их переменных окружения. """

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Аутентификация
AUTH_JWT_STRATEGY_SECRET = os.getenv('AUTH_JWT_STRATEGY_SECRET')
AUTH_JWT_MANAGER_SECRET = os.getenv('AUTH_JWT_MANAGER_SECRET')
ENCRYPTION_ALGORITHM = os.getenv('ENCRYPTION_ALGORITHM')

# Базы данных.
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')
db_uri = f'{user}:{password}@{host}:{port}/{database}'
async_db_engine_settings = f'postgresql+asyncpg://{db_uri}' \
                               f'?async_fallback=True'


# Рассылка электронных писем
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_SENDER = os.getenv('SMTP_SENDER')

# регистрация админа
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_TYPE = os.getenv('ADMIN_TYPE')

# Redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_URI = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
