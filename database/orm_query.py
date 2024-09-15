from cgitb import reset

from certifi import where
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product, Train


# //////////////////////       Train      ////////////
async def orm_add_train(session: AsyncSession, data: dict):
    date_new = Train(
        name=data['name'],
        description=data['description']
    )
    session.add(date_new)
    await session.commit()

async def orm_update_train(session: AsyncSession, names: str, data):
    query = update(Train).where(Train.name == names).values(
        name=data['name'],
        description=data['description']
        )
    await session.execute(query)
    await session.commit()

async def orm_select_train(session: AsyncSession):
    query = select(Train)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_where_select_train_name(session: AsyncSession, names: str):
    query = select(Train).where(Train.name == names)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_where_delete_train(session: AsyncSession, names: str):
    query = delete(Train).where(Train.name == names)
    await session.execute(query)
    await session.commit()


# /////////////////     Product      ///////////////
async def orm_add_act(session: AsyncSession, data: dict):
    obj = Product(
        name=data['name'],
        description=data['description'],
        types=data['type'],
        link=data['link'],
        date=data['date']
    )
    session.add(obj)
    await session.commit()


async def orm_update_product(session: AsyncSession, names: str, data):
    query = update(Product).where(Product.name == names).values(
        name=data['name'],
        description=data['description'],
        types=data['type'],
        link=data['link'],
        date=data['date']
        )
    await session.execute(query)
    await session.commit()

async def orm_select_act(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_where_select_act(session: AsyncSession, types: str):
    query = select(Product).where(Product.types == types)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_where_select_act_name(session: AsyncSession, names: str):
    query = select(Product).where(Product.name == names)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_where_delete_act(session: AsyncSession, names: str):
    query = delete(Product).where(Product.name == names)
    await session.execute(query)
    await session.commit()