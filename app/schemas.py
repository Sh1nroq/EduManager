from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    name:str = Field(..., min_length=2, max_length=50)
    avg_grade: Optional[float] = Field(None, ge=0, le=5)

class Student(StudentCreate):
    id:int
    group_id: int | None = None
    model_config = ConfigDict(from_attributes= True)

class StudentId(BaseModel):
    ok: bool = True
    student_id: int

class StudentList(BaseModel):
    data: List[Student]


class GroupCreate(BaseModel):
    name: str

class Group(GroupCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GroupId(BaseModel):
    ok: bool = True
    group_id: int

class GroupList(BaseModel):
    data: List[Group]

class UpdateStudentToGroup(BaseModel):
    student_id: int
    group_id: int

class GroupWithStudents(BaseModel):
    id: int
    name: str
    students: list[Student] = []

    model_config = ConfigDict(from_attributes=True)

class TransferStudent(BaseModel):
    student_id: int
    from_group_id: int
    to_group_id: int