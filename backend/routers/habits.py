from typing import List, Any, Coroutine, Dict

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from utils import get_session
from schemas.habit_schemas import HabitIn, HabitOut, HabitUpdate, SuccessResponse
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


@router.patch("/{id}", response_model=HabitOut)
async def update_habit_by_id(
        id: int = Path(..., description="id привычки"),
        habit_in: HabitUpdate = Depends(),
        session: AsyncSession = Depends(get_session)
) -> Habit:
    """Редактирование полей привычки"""
    result = await session.execute(select(Habit).where(id == Habit.id))
    habit = result.scalars().first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Обновляем только переданные НЕ None поля
    for k, v in habit_in.model_dump(exclude_unset=True).items():
        if v is not None:  # Исключаем None, чтобы не сломать NOT NULL колонки
            setattr(habit, k, v)

    await session.commit()
    return habit


@router.delete("/{id}", response_model=SuccessResponse)
async def update_habit_by_id(
        id: int = Path(..., description="id привычки"),
        session: AsyncSession = Depends(get_session)
) -> Dict[str, bool]:
    """Удаление привычки"""
    result = await session.execute(select(Habit).where(id == Habit.id))
    habit = result.scalars().first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    await session.delete(habit)
    await session.commit()
    return {"result": True}
