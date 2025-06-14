from typing import Dict, List, Any, Coroutine

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from databases.models import Habit, User
from schemas.habit_schemas import HabitIn, HabitOut, HabitUpdate, SuccessResponse
from utils import get_session

router = APIRouter(prefix="/api/habits")


@router.post("", response_model=HabitOut)
async def add_habit(habit: HabitIn, session=Depends(get_session)) -> Habit:
    """Добавление новой привычки"""
    new_habit: Habit = Habit(**habit.model_dump())
    session.add(new_habit)
    await session.commit()
    return new_habit


@router.get("", response_model=List[HabitOut])
async def get_habits(
        user_tg_id: int = Query(None, title="TG id user", description="User id for list habits", gt=0),
        session=Depends(get_session)
) -> Any | None:
    """
    Получение списка всех привычек
    :param user_tg_id: int Телеграмм id пользователя
    :param session: сессия
    :return: Список привычек для пользователя с user_tg_id | None
    """
    query = await session.execute(select(User).filter_by(tg_id=user_tg_id))
    user = query.scalars().first()
    if not user:
        return None
    res = await session.execute(select(Habit).filter_by(is_active=True, user_id=user.id))
    return res.scalars().all()


@router.get("/{id}", response_model=HabitOut)
async def get_habit_by_id(
        id: int = Path(..., description="id привычки"), session=Depends(get_session)
) -> Habit:
    """Получение привычки по id"""
    res = await session.execute(select(Habit).where(id == Habit.id))
    habit = res.scalars().first()
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit with {id} id, not found")
    return habit


@router.patch("/{id}", response_model=HabitOut)
async def update_habit_by_id(
        habit_in: HabitUpdate,
        id: int = Path(..., description="id привычки"),
        session: AsyncSession = Depends(get_session),
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
async def delete_habit_by_id(
        id: int = Path(..., description="id привычки"),
        session: AsyncSession = Depends(get_session),
) -> Dict[str, bool]:
    """Удаление привычки"""
    result = await session.execute(select(Habit).where(id == Habit.id))
    habit = result.scalars().first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    await session.delete(habit)
    await session.commit()
    return {"result": True}
