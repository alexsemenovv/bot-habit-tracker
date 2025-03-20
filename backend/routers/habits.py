from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.future import select

from utils import get_session
from schemas.habit_schemas import HabitIn, HabitOut
from databases.models import Habit

router = APIRouter(prefix='/api/habits')


@router.post("", response_model=HabitOut)
async def add_habit(habit: HabitIn, session=Depends(get_session)) -> Habit:
    """Добавление новой привычки"""
    new_habit: Habit = Habit(**habit.model_dump())
    session.add(new_habit)
    await session.commit()
    return new_habit


@router.get("", response_model=List[HabitOut])
async def get_habits(session=Depends(get_session)) -> List[Habit]:
    """Получение списка всех привычек"""
    res = await session.execute(select(Habit))
    return res.scalars().all()


@router.get("/{id}", response_model=HabitOut)
async def get_habit_by_id(
        id: int = Path(..., description="id привычки"),
        session=Depends(get_session)
) -> Habit:
    """Получение привычки по id"""
    res = await session.execute(select(Habit).where(id == Habit.id))
    return res.scalars().first()
