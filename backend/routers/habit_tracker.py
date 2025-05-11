from fastapi import APIRouter, Depends

from databases.models import HabitTrack
from schemas.habit_track_schemas import HabitTrackOut, HabitTrackIn
from utils import get_session

router = APIRouter(prefix="/api/habit_track")


@router.post("", response_model=HabitTrackOut)
async def add_habit(habit_track: HabitTrackIn, session=Depends(get_session)) -> HabitTrack:
    """Добавление новой модели 'Трек привычки' """
    new_habit_track: HabitTrack = HabitTrack(**habit_track.model_dump())
    session.add(new_habit_track)
    await session.commit()
    return new_habit_track
