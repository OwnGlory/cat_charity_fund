from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_projects import charity_projects_crud
from app.crud.investions import DataBaseWork
from app.schemas.charity_projects import (
    CharityProjectsCreate,
    CharityProjectsUpdate,
    CharityProjectsDB,
)
from app.api.validators import (
    check_name_duplicate, check_project_exists,
    check_project_open, check_project_full_amount,
    check_project_invested_amount, check_valid_name_for_project
)
from app.services.investions import invest_in_project
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectsDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectsCreate,
        session: AsyncSession = Depends(get_async_session)
):
    data_base_work = DataBaseWork(session)
    await check_valid_name_for_project(charity_project.name)
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_projects_crud.create(charity_project, session)
    await invest_in_project(new_project, data_base_work)
    session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectsDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    projects_from_db = await charity_projects_crud.get_multi(session)
    return projects_from_db


@router.patch(
    '/{project_id}',
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectsUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_project_exists(
        project_id, session
    )

    await check_project_open(charity_project)
    await check_project_full_amount(obj_in, charity_project)
    await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_projects_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_project_exists(
        project_id, session
    )
    await check_project_invested_amount(charity_project)
    charity_project = await charity_projects_crud.remove(
        charity_project, session
    )
    return charity_project

    # responses={
    #     status.HTTP_200_OK: {
    #         "model": CharityProjectsDB,
    #         "description": "Successful Response",
    #     },
    #     status.HTTP_400_BAD_REQUEST: {
    #         "model": ValidationError,
    #         "description": "Not unique name",
    #         "content": {
    #             "application/json": {
    #                 "example": {
    #                     "detail": "Проект с таким именем уже существует!",
    #                 }
    #             }
    #         }
    #     },
    #     status.HTTP_401_UNAUTHORIZED: {
    #         "model": ValidationError,
    #         "description": "Missing token or inactive user.",
    #         "content": {
    #             "application/json": {
    #                 "example": {
    #                     "detail": "Unauthorized",
    #                 }
    #             }
    #         }
    #     },
    #     status.HTTP_403_FORBIDDEN: {
    #         "model": ValidationError,
    #         "description": "Not a superuser.",
    #         "content": {
    #             "application/json": {
    #                 "example": {
    #                     "detail": "Forbidden",
    #                 }
    #             }
    #         }
    #     },
    # },