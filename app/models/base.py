from abc import ABCMeta
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta


class CustomMeta(ABCMeta, DeclarativeMeta):
    pass


class BaseData():
    full_amount = Column(Integer)  # Целочисленное поле > 0.
    invested_amount = Column(Integer, default=0)  # По умолчанию - 0.
    fully_invested = Column(Boolean, default=False)  # По умолчанию - False.
    created_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)