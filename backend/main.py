from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers.habit_tracker import router as habit_track_router
from routers.habits import router as habit_router
from routers.users import router as user_router
from utils import create_tables


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
app.include_router(habit_track_router)
