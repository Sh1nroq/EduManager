from typing import Optional

from sqlalchemy import select, delete, update

from app.schemas import StudentCreate, Student, UpdateStudentToGroup, TransferStudent
from app.database import new_session, StudentsOrm, GroupOrm


class StudentRepository:
    @classmethod
    async def add_one(cls, data: StudentCreate) -> int:
        async with new_session() as session:
            student_dict = data.model_dump()

            student = StudentsOrm(**student_dict)
            session.add(student)
            await session.flush()
            await session.commit()
            return student.id

    @classmethod
    async def get_all(cls) -> list[Student]:
        async with new_session() as session:
            query = select(StudentsOrm)
            result = await session.execute(query)
            student_models = result.scalars().all()
            return student_models

    @classmethod
    async def get_one(cls, student_id:int) -> Optional[StudentsOrm]:
        async with new_session() as session:
            query = select(StudentsOrm).where(StudentsOrm.id == student_id)
            result = await session.execute(query)
            student_model = result.scalars().first()
            return student_model

    @classmethod
    async def del_student(cls, student_id:int):
        async with new_session() as session:
            query = delete(StudentsOrm).where(StudentsOrm.id == student_id).returning(StudentsOrm.id)
            result = await session.execute(query)
            deleted_id = result.scalar_one_or_none()

            await session.commit()
            return deleted_id

    @classmethod
    async def add_student_to_group(cls, data: UpdateStudentToGroup):
        async with new_session() as session:
            student = await session.get(StudentsOrm, data.student_id)
            if not student:
                return "student_not_found"

            if student.group_id is not None:
                return "already_has_group"

            group = await session.get(GroupOrm, data.group_id)
            if not group:
                return "group_not_found"

            student.group_id = data.group_id
            await session.commit()
            return "success"

    @classmethod
    async def del_student_from_group(cls, data: UpdateStudentToGroup):
        async with new_session() as session:
            query = update(StudentsOrm).where(StudentsOrm.id == data.student_id).values(group_id=None)
            await session.execute(query)
            await session.commit()
            return True

    @classmethod
    async def switch_group(cls, data: UpdateStudentToGroup) -> bool:
        async with new_session() as session:
            query = (update(StudentsOrm).where(StudentsOrm.id == data.student_id).values(group_id=data.group_id))

            result = await session.execute(query)
            await session.commit()

            return result.rowcount > 0

    @classmethod
    async def transfer_student_logic(cls, data: TransferStudent) -> str:
        async with new_session() as session:
            student = await session.get(StudentsOrm, data.student_id)
            if not student:
                return "student_not_found"

            if student.group_id != data.from_group_id:
                return "wrong_source_group"

            if data.from_group_id == data.to_group_id:
                return "same_group"

            target_group = await session.get(GroupOrm, data.to_group_id)
            if not target_group:
                return "target_group_not_found"

            student.group_id = data.to_group_id
            await session.commit()
            return "success"