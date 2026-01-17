from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_async_engine(DB_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class StudentsOrm(Model):
    __tablename__ = "Students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    avg_grade: Mapped[Optional[float]]

    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Groups.id"))
    group: Mapped["GroupOrm"] = relationship(back_populates="students")

class GroupOrm(Model):
    __tablename__ = "Groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    students: Mapped[list["StudentsOrm"]] = relationship(back_populates="group")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)