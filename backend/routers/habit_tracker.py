from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from databases.models import HabitTrack
from schemas.habit_track_schemas import HabitTrackIn, HabitTrackOut, SuccessResponse
from utils import get_session

router = APIRouter(prefix="/api/habits_track")


@router.post("", response_model=HabitTrackOut)
async def add_habit_track(
    habit_track: HabitTrackIn, session=Depends(get_session)
) -> HabitTrack:
    """Добавление новой модели 'Трек привычки'"""
    new_habit_track: HabitTrack = HabitTrack(**habit_track.model_dump())
    session.add(new_habit_track)
    await session.commit()
    return new_habit_track


@router.get("", response_model=List[HabitTrackOut])
async def get_habit_tracks(session=Depends(get_session)) -> List[HabitTrack]:
    """Получение списка всех треков привычек"""
    res = await session.execute(select(HabitTrack))
    return res.scalars().all()


@router.get("/{id}", response_model=HabitTrackOut)
async def get_habit_track_by_id(
    id: int = Path(..., description="id трека привычки"), session=Depends(get_session)
) -> HabitTrack:
    """Получение трека привычки по id"""
    res = await session.execute(select(HabitTrack).where(id == HabitTrack.id))
    habit_track = res.scalars().first()
    if not habit_track:
        raise HTTPException(status_code=404, detail="HabitTrack not found")
    return habit_track


@router.delete("/{id}", response_model=SuccessResponse)
async def delete_habit_track_by_id(
    id: int = Path(..., description="id трека привычки"),
    session: AsyncSession = Depends(get_session),
) -> Dict[str, bool]:
    """Удаление трека привычки"""
    result = await session.execute(select(HabitTrack).where(id == HabitTrack.id))
    habit_track = result.scalars().first()
    if not habit_track:
        raise HTTPException(status_code=404, detail="HabitTrack not found")
    await session.delete(habit_track)
    await session.commit()
    return {"result": True}
