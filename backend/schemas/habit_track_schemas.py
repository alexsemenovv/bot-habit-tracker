from datetime import date

from pydantic import BaseModel


class BaseHabitTrack(BaseModel):
    """Базовая схема 'Трек привычки'"""

    habit_id: int
    date_of_completion: date


class HabitTrackIn(BaseHabitTrack):
    """Схема 'Трек привычки' на вход"""

    ...


class HabitTrackOut(BaseHabitTrack):
    """Схема 'Трек привычки' на выход"""

    id: int

    model_config = {"from_attributes": True}


class SuccessResponse(BaseModel):
    """Схема: успешный ответ"""

    result: bool
