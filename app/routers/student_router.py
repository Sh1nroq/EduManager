from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from typing import Annotated

from app.database import StudentsOrm
from app.repositories.student_repo import StudentRepository
from app.schemas import StudentCreate, StudentId, Student, StudentList, UpdateStudentToGroup, TransferStudent

student_router = APIRouter(
    prefix = "/students",
    tags = ["Main"],
)

@student_router.post("/")
async def add_student(student: Annotated[StudentCreate, Depends()]) -> StudentId:
    student_id = await StudentRepository.add_one(student)
    return StudentId(student_id=student_id)

@student_router.get("/")
async def get_all_students() -> StudentList:
    students = await StudentRepository.get_all()
    return StudentList(data=students)

@student_router.get("/{student_id}", response_model=Student)
async def get_one_student(student_id:int) -> StudentsOrm:
    student_model = await StudentRepository.get_one(student_id)
    if student_model is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_model

@student_router.delete("/delete/{student_id}")
async def del_one_student(student_id: int) -> dict:
    del_model = await StudentRepository.del_student(student_id)
    if del_model is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"status": "success", "id": del_model}


@student_router.post("/add_student_to_group")
async def add_student_to_group(data: UpdateStudentToGroup):
    result = await StudentRepository.add_student_to_group(data)

    if result == "student_not_found":
        raise HTTPException(status_code=404, detail="Студент не найден")

    if result == "group_not_found":
        raise HTTPException(status_code=404, detail="Целевая группа не существует")

    if result == "already_has_group":
        raise HTTPException(
            status_code=400,
            detail="Студент уже зачислен в группу. Для смены группы используйте /transfer"
        )

    return {"ok": True, "message": "Добавлен успешно"}
@student_router.delete("/delete_from_group")
async def del_student_to_group(data: UpdateStudentToGroup):
    result = await StudentRepository.del_student_from_group(data)
    if not result:
        raise HTTPException(status_code=400, detail="fatal error: cant update db")
    return {"ok": True, "message": f"Student {data.student_id} deleted from group {data.group_id}"}

@student_router.patch("/transfer")
async def transfer_student(data: TransferStudent):
    result = await StudentRepository.transfer_student_logic(data)

    if result == "student_not_found":
        raise HTTPException(status_code=404, detail="Студент не найден")
    if result == "wrong_source_group":
        raise HTTPException(status_code=400, detail="Студент сейчас находится в другой группе")
    if result == "same_group":
        raise HTTPException(status_code=400, detail="Нельзя перевести студента в ту же самую группу")
    if result == "target_group_not_found":
        raise HTTPException(status_code=404, detail="Целевая группа не существует")

    return {"ok": True, "message": "Студент успешно переведен"}