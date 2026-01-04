from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from typing import Annotated

from app.database import GroupOrm
from app.repositories.group_repo import GroupRepository
from app.schemas import GroupCreate, GroupId, GroupList, Group, GroupWithStudents

group_router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)

@group_router.post("/")
async def add_group(group: Annotated[GroupCreate, Depends()]) -> GroupId:
    result = await GroupRepository.add_group(group)

    if result == "already_exists":
        raise HTTPException(status_code=400,detail=f"Группа с названием '{group.name}' уже существует")

    return GroupId(group_id=result)

@group_router.delete("/delete/{group_id}")
async def del_group(group_id: int) -> dict:
    del_model = await GroupRepository.del_group(group_id)
    if del_model is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"status": "success", "id": del_model}

@group_router.get("/")
async def get_list_groups() -> GroupList:
    groups = await GroupRepository.get_all()
    return GroupList(data=groups)

@group_router.get("/{group_id}", response_model=Group)
async def get_one_group(group_id:int) -> GroupOrm:
    group_model = await GroupRepository.get_one(group_id)
    if group_model is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group_model

@group_router.get("/{group_id}/students", response_model=GroupWithStudents)
async def get_students_in_group(group_id: int):
    group = await GroupRepository.get_group_detailed(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return group