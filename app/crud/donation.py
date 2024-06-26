from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    async def get_donations_by_user_id(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> list[Donation]:
        db_user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        return db_user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)


# async def create_donation(
#     new_donation: DonationCreate,
#     session: AsyncSession,
# ) -> Donation:
#     new_donation_data = new_donation.dict()
#     db_donation = Donation(**new_donation_data)
#     session.add(db_donation)
#     await session.commit()
#     await session.refresh(db_donation)
#     return db_donation
#
#
# async def read_all_donations_for_project(
#     session: AsyncSession,
# ) -> list[Donation]:
#     donations_from_db = await session.execute(
#         select(Donation)
#     )
#     donations_from_db = donations_from_db.scacalrs().all()
#     return donations_from_db