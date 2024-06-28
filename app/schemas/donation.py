from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Field, Extra, PositiveInt
)


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
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
    full_amount: PositiveInt


class DonationAllDB(DonationBase):
    id: Optional[int]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDB(DonationAllDB):
    user_id: Optional[int]
    invested_amount: Optional[int] = Field(0)
    fully_invested: Optional[bool] = Field(False)
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
