from sqlalchemy import (
    Column,
    String,
    Text
)
from app.core.db import Base


class CharityProjects(Base):
    """
    Модель таблицы благотворительных проектов.
    """
    name = Column(String(100), unique=True, nullable=False)  # Уникальное название проекта
    description = Column(Text, nullable=False)  # Описание. Добавить проверку на > 1 символа и обязательное поле
