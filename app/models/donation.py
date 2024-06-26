from sqlalchemy import (
    Column,
    Integer,
    Text,
    # ForeignKey,
)
from app.core.db import Base


class Donation(Base):
    """
    Модель таблицы пожертвований.
    """
    user_id = Column(Integer,)  # Id пользователя. ForeignKey из Users.
    comment = Column(Text, nullable=True)  # Комментарий. Необязательное поле.
