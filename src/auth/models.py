from datetime import datetime
import enum
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

# from .schemas import UserSchema
from src.core.database import Base


class UserType(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=False, nullable=False)
    email = Column(String(320), unique=True, index=True, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    hashed_password = Column(String(1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    # Связь с таблицей приватных шаблонов
    # private_templates = relationship(
    #     PrivateTemplate, back_populates='owner', cascade='all, delete-orphan',
    # )

    def __repr__(self) -> str:
        return f'User {self.id}: {self.username}'

    # def to_read_model(self):
    #     return UserSchema(
    #         id=self.id,
    #         email=self.email,
    #         username=self.username,
    #         organization=self.organization,
    #         user_type=self.user_type
    #     )
