from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("postgresql+asyncpg://postgres:123321@localhost:5432/EduManagerDB")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class StudentsOrm(Model):
    __tablename__ = "Students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    avg_grade: Mapped[Optional[float]]

class GroupOrm(Model):
    __tablename__ = "Groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)