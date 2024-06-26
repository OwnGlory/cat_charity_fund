from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_projects import charity_projects_crud
from app.models import CharityProjects
from app.schemas.validators import ValidationError


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project_id = await charity_projects_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(status_code=404, detail=ValidationError(
            message="Проект с таким именем уже существует!").dict()
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProjects:
    charity_project = await charity_projects_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка не найдена!'
        )
    return charity_project
