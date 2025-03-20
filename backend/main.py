from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils import create_tables, drop_tables
from routers.habits import router as habit_router
from routers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Создание таблиц перед запуском приложения,
    и закрытие соединения после
    """
    await create_tables()
    yield
    # await drop_tables()


app = FastAPI(lifespan=lifespan)

app.include_router(habit_router)
app.include_router(user_router)
