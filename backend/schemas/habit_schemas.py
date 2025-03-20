from typing import Optional
from datetime import date

from pydantic import BaseModel


class BaseHabit(BaseModel):
    """Базовая схема привычки"""
    name: str
    description: Optional[str] = None
    start_date: date
    user_id: int


class HabitIn(BaseHabit):
    """Схема 'привычка' на вход"""
    ...


class HabitOut(BaseHabit):
    """Схема 'привычка' на выход"""
    id: int

    model_config = {
        "from_attributes": True
    }