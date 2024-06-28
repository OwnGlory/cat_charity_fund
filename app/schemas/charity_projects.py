from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, Extra


class CharityProjectsBase(BaseModel):

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "name": "Первый проект",
                "description": "Проект для пожертвований",
                "full_amount": 1000
            }
        }


class CharityProjectsCreate(CharityProjectsBase):
    name: str = Field(
        ..., max_length=100,
        title='Название проекта',
        description='Уникальное названние проекта'
    )
    description: str = Field(..., min_length=2)
    full_amount: int = Field(..., gt=0)


class CharityProjectsUpdate(CharityProjectsBase):
    id: int
    name: Optional[str] = Field(
        None, max_length=100,
        title='Название проекта',
        description='Уникальное названние проекта'
    )
    description: Optional[str] = Field(None, min_length=2)
    full_amount: Optional[int] = Field(None, gt=0)

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class CharityProjectsDB(BaseModel):
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