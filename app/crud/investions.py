# app/crud/investions.py
from sqlalchemy.orm import Session
from sqlalchemy import select


class DataBaseWork:
    def __init__(self, session: Session):
        self.session = session

    async def insert(self, obj):
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

    async def insert_many(self, first_obj, second_obj):
        self.session.add_all([first_obj, second_obj])
        await self.session.commit()
        await self.session.refresh(first_obj)
        await self.session.refresh(second_obj)

    def find(self, model):
        result = self.session.execute(
            select(model).where(
                model.fully_invested == 0
            )
        )
        return result
