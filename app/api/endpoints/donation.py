from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import (
    DonationCreate,
    # DonationDB,
)

from app.core.db import get_async_session
from app.crud.donation import donation_crud

router = APIRouter()


@router.post(
    '/'
    # response_model=DonationDB,
    # response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(donation, session)
    return new_donation


@router.get(
    '/',
)
async def get_all_donation_info(
    session: AsyncSession = Depends(get_async_session)
):
    donation_from_db = await donation_crud.get_multi(session)
    return donation_from_db


@router.get(
    '/{my}'
    # response_model=DonationDB,
)
async def get_user_donation_info(
        my: int,
        session: AsyncSession = Depends(get_async_session)
):
    user_donation = await donation_crud.get_donations_by_user_id(
        my, session
    )
    if user_donation is None:
        raise HTTPException(
            status_code=404,
            detail='Пожертвований пока нету.'
        )
    return user_donation
