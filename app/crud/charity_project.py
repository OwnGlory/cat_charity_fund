from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.models import CharityProject
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        # db_obj = await session.execute(
        #     select(self.model).where(
        #         self.model.id == obj_id
        #     )
        # )
        db_obj = await session.get(self.model, obj_id)
        return db_obj

    async def create(
            self,
            obj_in,
            session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()


charity_projects_crud = CRUDCharityProject(CharityProject)

# async def create_charity_projects(
#     new_project: CharityProjectsCreate,
#     session: AsyncSession,
# ) -> CharityProjects:
#     new_project_data = new_project.dict()
#     db_project = CharityProjects(**new_project_data)
#     session.add(db_project)
#     await session.commit()
#     await session.refresh(db_project)
#     return db_project
#
#
# async def read_all_projects_from_db(
#     session: AsyncSession,
# ) -> list[CharityProjects]:
#     projects_from_db = await session.execute(
#         select(CharityProjects)
#     )
#     projects_from_db = projects_from_db.scacalrs().all()
#     return projects_from_db
#
# # Пример
# async def get_project_by_id(
#     project_id: int,
#     session: AsyncSession,
# ) -> Optional[CharityProjects]:
#     project_by_id = await session.get(CharityProjects, project_id)
#     return project_by_id
#
# async def update_charity_project(
#         # Объект из БД для обновления.
#         db_project: CharityProjects,
#         # Объект из запроса.
#         project_in: CharityProjectsUpdate,
#         session: AsyncSession,
# ) -> CharityProjects:
#     # Представляем объект из БД в виде словаря.
#     obj_data = jsonable_encoder(db_project)
#     # Конвертируем объект с данными из запроса в словарь,
#     # исключаем неустановленные пользователем поля.
#     update_data = project_in.dict(exclude_unset=True)
#
#     # Перебираем все ключи словаря, сформированного из БД-объекта.
#     for field in obj_data:
#         # Если конкретное поле есть в словаре с данными из запроса, то...
#         if field in update_data:
#             # ...устанавливаем объекту БД новое значение атрибута.
#             setattr(db_project, field, update_data[field])
#     # Добавляем обновленный объект в сессию.
#     session.add(db_project)
#     # Фиксируем изменения.
#     await session.commit()
#     # Обновляем объект из БД.
#     await session.refresh(db_project)
#     return db_project
#
#
# async def delete_charity_project(
#         db_project: CharityProjects,
#         session: AsyncSession,
# ) -> CharityProjects:
#     # Удаляем объект из БД.
#     await session.delete(db_project)
#     # Фиксируем изменения в БД.
#     await session.commit()
#     # Не обновляем объект через метод refresh(),
#     # следовательно он всё ещё содержит информацию об удаляемом объекте.
#     return db_project