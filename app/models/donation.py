from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
)
from app.models.base import BaseData
from app.core.db import Base


class Donation(BaseData, Base):
    """
    Модель таблицы пожертвований.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
