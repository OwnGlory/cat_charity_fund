from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Field, Extra, PositiveInt
)


class DonationBase(BaseModel):
    """Базовая схема для пожертвований."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "full_amount": 100,
                "comment": "Мое первое пожертвование",

            }
        }


class DonationCreate(DonationBase):
    """Схема для созданий пожертвований."""
    pass


class DonationAllDB(DonationBase):
    """
    Схема для вывода информации при создании пожертвования
    и получении пожертвований пользователя.
    """
    id: Optional[int]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDB(DonationAllDB):
    """Схема для получения всех пожертвований."""
    user_id: Optional[int]
    invested_amount: Optional[int] = Field(0)
    fully_invested: Optional[bool] = Field(False)
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
