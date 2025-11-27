from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.sql.annotation import Annotated

from repository import StudentRepository
from schemas import StudentCreate

router = APIRouter(
    prefix = "/students"
)


@router.post("")
async def add_student(
        student: Annotated[StudentCreate, Depends()],
):
    student_id = await StudentRepository.add_one(student)
    return {"ok": True, "student_id": student_id}

@router.get("")
async def get_all_students():
    students = await StudentRepository.get_all()
    return {"data": students}