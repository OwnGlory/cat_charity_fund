from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Field, Extra, PositiveInt
)


class DonationBase(BaseModel):
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
    full_amount: PositiveInt
    # create_date: Optional[datetime] = Field(datetime.now)


class DonationDB(DonationBase):
    full_amount: Optional[PositiveInt]
    comment: Optional[str] = Field("Комментарий")
    id: Optional[int]
    create_date: Optional[datetime]
    user_id: Optional[int]
    invested_amount: Optional[int] = Field(0)
    fully_invested: Optional[bool] = Field(False)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationAllDB(DonationBase):
    full_amount: int
    comment: Optional[str]
    id: Optional[int]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True
