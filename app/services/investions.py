from datetime import datetime

from app.models import CharityProject, Donation
from app.crud.investions import DataBaseWork


async def invest_donation(
        donation: Donation,
        data_base_work: DataBaseWork
):
    """Функция распределения пожертвований по незакрытым проектам."""
    not_invested_projects = await data_base_work.find(model=CharityProject)
    not_invested_projects = not_invested_projects.scalars().all()
    await investment_process(donation, not_invested_projects, data_base_work)


async def invest_in_project(
        project: CharityProject,
        data_base_work: DataBaseWork
):
    """Функция распределения свободных сумм."""
    not_invested_donations = await data_base_work.find(model=Donation)
    not_invested_donations = not_invested_donations.scalars().all()
    await investment_process(project, not_invested_donations, data_base_work)


def close_process(obj):
    """Общая функция закрытия."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


def close_many_processes(objs):
    """Функция закрытия для множества объектов."""
    for obj in objs:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def investment_process(
        obj_in,
        not_invested_obj_list,
        data_base_work: DataBaseWork
):
    """Общая функция инвестирования."""

    if not not_invested_obj_list:
        return "ПУСТО!"

    for obj in not_invested_obj_list:
        if obj_in.fully_invested is False and obj is not None:
            obj_in_balance = obj_in.full_amount - obj_in.invested_amount
            obj_balance = obj.full_amount - obj.invested_amount
            if obj_in_balance < obj_balance:
                obj.invested_amount += obj_in_balance
                obj_in.invested_amount += obj_in_balance
                close_process(obj_in)
                await data_base_work.insert(obj)
                await data_base_work.insert(obj_in)
            elif obj_in_balance > obj_balance:
                obj_in.invested_amount += obj_balance
                obj.invested_amount += obj_balance
                close_process(obj)
                await data_base_work.insert(obj)
                await data_base_work.insert(obj_in)
            elif obj_balance == obj_in_balance:
                obj_in.invested_amount += obj_balance
                obj.invested_amount += obj_balance
                close_many_processes([obj, obj_in])
                await data_base_work.insert(obj)
                await data_base_work.insert(obj_in)
