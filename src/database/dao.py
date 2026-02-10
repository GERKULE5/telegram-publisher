# src/database/dao/py
from typing import Optional, List, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


from database.database import async_connection
from database.models import Admin, Channel, AuthorizedUser



@async_connection
async def get_admin(session: AsyncSession, user_id: int):
    try:
        return await session.get(Admin, user_id)
    except SQLAlchemyError as e:
        print(f'Error: {e}')

@async_connection 
async def authorize_user(session: AsyncSession, user: AuthorizedUser):
    try:
        return await session.add(user)
    except SQLAlchemyError as e:
        print(f'Error: {e}')
        session.rollback()
