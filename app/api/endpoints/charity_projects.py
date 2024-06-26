from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_projects import charity_projects_crud
from app.schemas.charity_projects import (
    CharityProjectsCreate,
    CharityProjectsUpdate,
    CharityProjectsDB,
)
from app.api.validators import (
    check_name_duplicate, check_project_exists
)

router = APIRouter()


@router.post('/', response_model=CharityProjectsDB)
async def create_new_charity_project(
        charity_project: CharityProjectsCreate,
        session: AsyncSession = Depends(get_async_session)
):
    print(charity_project.name)
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_projects_crud.create(charity_project, session)
    return new_project


@router.get(
    '/'
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    projects_from_db = await charity_projects_crud.get_multi(session)
    return projects_from_db


@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    '/{project_id}'
)
async def partially_update_charity_project(
        # ID обновляемого объекта.
        project_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: CharityProjectsUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    # Выносим повторяющийся код в отдельную корутину.
    charity_project = await check_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_projects_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}'
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    # Выносим повторяющийся код в отдельную корутину.
    charity_project = await check_project_exists(
        project_id, session
    )
    charity_project = await charity_projects_crud.remove(
        charity_project, session
    )
    return charity_project
