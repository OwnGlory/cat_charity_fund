from sqlalchemy import (
    Column,
    String,
    Text
)

from app.models.base import BaseData
from app.core.db import Base


class CharityProject(BaseData, Base):
    """
    Модель таблицы благотворительных проектов.
    """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Проект {self.name} уже полностью инвестирован'
        )