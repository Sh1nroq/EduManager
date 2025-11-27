from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import delete_tables, create_tables
from router import router as student_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await delete_tables()
    print("База данных очищена!")
    await create_tables()
    print("База данных создана!")
    yield
    print("Завершение!")

app = FastAPI(lifespan = lifespan)
app.include_router(student_router)
