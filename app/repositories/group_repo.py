from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.schemas import GroupCreate, Group
from app.database import new_session, GroupOrm


class GroupRepository:
    @classmethod
    async def add_group(cls, data: GroupCreate):
        async with new_session() as session:
            try:
                group_dict = data.model_dump()
                group = GroupOrm(**group_dict)
                session.add(group)
                await session.flush()
                await session.commit()
                return group.id
            except IntegrityError:
                await session.rollback()
                return "already_exists"

    @classmethod
    async def del_group(cls, group_id: int):
        async with new_session() as session:
            query = delete(GroupOrm).where(GroupOrm.id == group_id).returning(GroupOrm.id)
            result = await session.execute(query)
            deleted_id = result.scalar_one_or_none()
            await session.commit()
            return deleted_id

    @classmethod
    async def get_all(cls) -> list[Group]:
        async with new_session() as session:
            query = select(GroupOrm)
            result = await session.execute(query)
            group_models = result.scalars().all()
            return group_models

    @classmethod
    async def get_one(cls, group_id:int) -> Optional[GroupOrm]:
        async with new_session() as session:
            query = select(GroupOrm).where(GroupOrm.id == group_id)
            result = await session.execute(query)
            group_model = result.scalars().first()
            return group_model

    @classmethod
    async def get_group_detailed(cls, group_id: int):
        async with new_session() as session:
            query = (
                select(GroupOrm)
                .options(joinedload(GroupOrm.students))
                .where(GroupOrm.id == group_id)
            )
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

