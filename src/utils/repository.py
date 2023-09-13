import json
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

import aioredis
from pydantic.json import pydantic_encoder
from sqlalchemy import insert, select

from src.core.config import REDIS_URI as redis_uri
from src.core.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, data: dict = None):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, obj, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def create_all(self, objects: list):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """Базовый класс для работы с БД."""

    model = None

    async def add_one(self, data: dict) -> dict:
        """
        Добавляет 1 элемент в базу по словарю
        :param data: значения, которые нужно добавить
        :return: id
        """
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self, data: dict = None):
        """
        Получает все объекты по фильтру.
        :param data: Словарь с данными фильтров
        :return: Список объектов.
        """
        async with async_session_maker() as session:
            if data:
                stmt = select(self.model).filter_by(**data)
            else:
                stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def get_one(self, data: dict):
        """
        Получает один элемент из базы по словарю
        :param data: словарь, по которому нужно получить элемент
        """
        async with async_session_maker() as session:
            condition = []
            for key, value in data.items():
                condition.append(self.model.__table__.c[key] == value)
            # Составляем запрос с указанными условиями
            query = select(self.model).where(*condition)
            # Выполняем запрос и возвращаем результат
            result = await session.scalar(query)
            if result:
                return result

    async def update_one(self, obj, data: dict):
        """
        Обновляет элемент
        :param data: новые данные
        :param obj: объект, который нужно обновить
        """
        async with async_session_maker() as session:
            for key, value in data.items():
                setattr(obj, key, value)
            session.add(obj)
            await session.commit()

    async def delete_one(self, obj):
        """
        Удаление объекта
        :param obj: Объект для удаления.
        """
        async with async_session_maker() as session:
            await session.delete(obj)
            await session.commit()

    async def create_all(self, objects: list):
        """
        Массовое добавление объектов.
        :param objects: Список объектов
        """
        async with async_session_maker() as session:
            session.add_all(objects)
            await session.commit()


# class RedisRepository:
#     @asynccontextmanager
#     async def _redis_connection(self, redis_uri) -> None:
#         # Открываем соединение с Redis
#         redis_client = await aioredis.from_url(redis_uri)
#         try:
#             # Возвращаем соединение в блок `with`
#             yield redis_client
#         finally:
#             # Закрываем соединение с Redis при выходе из блока `with`
#             await redis_client.close()
#
#     async def _convert_bytes_to_str(self, data: dict) -> dict:
#         """Преобразование данных из байтового представления в строки."""
#         converted_data = {}
#         for key, value in data.items():
#             # Декодирование байтового значения в строку (UTF-8)
#             converted_data[key.decode()] = value.decode()
#         return converted_data
#
#     async def add_one(self, token, data: dict) -> None:
#         """
#         Добавляет в redis данные
#         :param token: ключ
#         :param data: значение
#         :param remember_me: запомнить меня
#         """
#         remember_me = bool(int(data.get('remember_me')))
#         async with self._redis_connection(redis_uri) as redis_client:
#             # Проверка, что сессии с таким session_id не существует
#             if await redis_client.exists(token):
#                 raise BackendError("create can't overwrite an existing session")
#             await redis_client.hmset(token, data)
#             if remember_me is True:
#                 await redis_client.expire(token, 7 * 60 * 60)
#             else:
#                 await redis_client.expire(token, 30 * 60)
#
#     async def add_cache(self, key: str, value, expire=None) -> None:
#         """
#         Добавление в кэш
#         :param key: Ключ записи
#         :param value: Значение
#         :param expire: Время кеша
#         """
#         async with self._redis_connection(redis_uri) as redis_client:
#             if not expire:
#                 encoded_response = json.dumps(value, default=pydantic_encoder)
#                 await redis_client.set(key, encoded_response)
#             else:
#                 await redis_client.set(key, value)
#                 await redis_client.expire(key, expire)
#
#     async def get_cache(self, key: str) -> bytes:
#         """
#         Получение данных из кэша
#         :param key: Ключ записи
#         """
#         async with self._redis_connection(redis_uri) as redis_client:
#             data = await redis_client.get(key)
#             return data
#
#     async def get_one(self, token, *args) -> dict:
#         async with self._redis_connection(redis_uri) as redis_client:
#             data = await redis_client.hgetall(str(token))
#             if not data:
#                 raise BackendError("Incorrect token")
#             session_data = await self._convert_bytes_to_str(data)
#             return session_data
#
#     async def del_one(self, token) -> bool:
#         async with self._redis_connection(redis_uri) as redis_client:
#             # Удаление сессии по token
#             deleted = await redis_client.delete(str(token))
#
#             return bool(deleted)
#
#     async def update_one(self, old_token, new_token):
#         """
#         Удаление сессии с old_token и создание сессии с new_token
#         """
#         session_data = await self.get_one(old_token)
#         await self.del_one(old_token)
#         await self.add_one(new_token, session_data)
#         return new_token
