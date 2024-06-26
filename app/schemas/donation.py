from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Field,
)


class DonationBase(BaseModel):
    full_amount: Optional[int] = Field(None, gt=0)
    comment: Optional[str]


class DonationCreate(DonationBase):
    full_amount: int = Field(..., gt=0)


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAllDB(DonationDB):
    user_id: int
    invested_amount: int = Field(0,)
    fully_invested: bool = Field(False,)
    close_date: Optional[datetime]