from typing import Optional
from datetime import date

from pydantic import BaseModel


class BaseHabit(BaseModel):
    """Базовая схема привычки"""
    name: str
    description: Optional[str] = None
    start_date: date


class HabitIn(BaseHabit):
    """Схема на вход"""
    ...


class HabitOut(BaseHabit):
    """Схема на выход"""
    id: int

    class Config:
        """Класс HabitOut будет использоваться для сериализации ORM"""
        orm_mode = True
