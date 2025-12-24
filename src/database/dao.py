# src/database/dao/py
from typing import Optional, List, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


from database.database import async_connection
from database.models import Admin, Institution, Channel



@async_connection
async def get_admin(session: AsyncSession, user_id: int):
    try:
        return await session.get(Admin, user_id)
    except SQLAlchemyError as e:
        print(f'Error: {e}')

    
@async_connection
async def get_institution_by_code(session: AsyncSession, code: str):
    try:
        stmt = select(Institution).where(Institution.code==code)
        result = await session.execute(stmt)
        institution = result.scalar_one_or_none()
        return institution
    except SQLAlchemyError as e:
        await session.rollback()
        print(f'Error: {e}')
        return None



