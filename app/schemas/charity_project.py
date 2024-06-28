from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, Extra


class CharityProjectBase(BaseModel):

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "name": "Первый проект",
                "description": "Проект для пожертвований",
                "full_amount": 1000
            }
        }


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., min_length=1, max_length=100,
        title='Название проекта',
        description='Уникальное названние проекта'
    )
    description: str = Field(..., min_length=2)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]


class CharityProjectDB(BaseModel):
    name: Optional[str] = Field("Название проекта")
    description: Optional[str] = Field("Описание проекта")
    full_amount: Optional[int] = Field(0)
    id: Optional[int] = Field(0)
    invested_amount: Optional[int] = Field(0)
    fully_invested: Optional[bool] = Field(False)
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True