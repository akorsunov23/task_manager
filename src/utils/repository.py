from abc import ABC, abstractmethod

from sqlalchemy import insert, select

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


class SQLAlchemyRepository(AbstractRepository):
    """Базовый класс для работы с БД."""

    model = None

    async def add_one(self, data: dict) -> dict:
        """
        Добавляет 1 элемент в базу по словарю.
        :param data: Значения, которые нужно добавить.
        :return: Id.
        """
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self, data: dict = None):
        """
        Получает все объекты по фильтру.
        :param data: Словарь с данными фильтров.
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
        Получает один элемент из базы по словарю.
        :param data: Словарь, по которому нужно получить элемент.
        """
        async with async_session_maker() as session:
            condition = []
            for key, value in data.items():
                condition.append(self.model.__table__.c[key] == value)
            query = select(self.model).where(*condition)
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
        Удаление объекта.
        :param obj: Объект для удаления.
        """
        async with async_session_maker() as session:
            await session.delete(obj)
            await session.commit()
