from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import delete_tables, create_tables
from router import student_router, group_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await delete_tables()
    print("База данных очищена!")
    await create_tables()
    print("База данных создана!")
    print("Бэк поднят!")
    yield
    print("Завершение!")

app = FastAPI(lifespan = lifespan)
app.include_router(student_router)
app.include_router(group_router)
