from sqlalchemy import select
from schemas import StudentCreate, Student
from database import new_session, StudentsOrm


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

    async def get_all(cls) -> list[Student]:
        async with new_session() as session:
            query = select(StudentsOrm)
            result = await session.execute(query)
            student_models = result.scalars().all()
            return student_models