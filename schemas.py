from typing import Optional
from pydantic import BaseModel, ConfigDict

class StudentCreate(BaseModel):
    name:str
    description: Optional[str] = None

class Student(StudentCreate):
    id:int

    model_config = ConfigDict(from_attributes= True)

class StudentId(BaseModel):
    ok: bool = True
    student_id: int