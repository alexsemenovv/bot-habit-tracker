from datetime import datetime as dt

from databases.database import Base
from sqlalchemy import (
    VARCHAR,
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship


class User(Base):
    """Сущность: пользователь"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR(100), index=True, nullable=False)
    last_name = Column(VARCHAR(100), index=True, nullable=True)
    username = Column(VARCHAR(100), index=True, nullable=False)
    tg_id = Column(BigInteger, index=True, nullable=False)
    is_bot = Column(Boolean, default=False, nullable=False)

    habits = relationship("Habit", back_populates="user")

    def __str__(self) -> str:
        return f"Пользователь {self.first_name} {self.username}"


class Habit(Base):
    """Сущность: привычка"""

    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(50), index=True, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False, default=dt.date(dt.now()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_days = Column(Integer, nullable=False, default=21)
    is_active = Column(Boolean, nullable=True, default=True, index=True)

    user = relationship("User", back_populates="habits")
    habit_track = relationship("HabitTrack", back_populates="habit")

    def __str__(self) -> str:
        return f"Привычка: {self.name}\nДата начала: {dt.strftime(self.start_date, '%d-%m-%Y')}"


class HabitTrack(Base):
    """Отслеживает невыполнение/выполнение привычки в этот день"""

    __tablename__ = "habit_track"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    date_of_completion = Column(Date, nullable=False, default=dt.date(dt.now()))
    is_done = Column(Boolean, nullable=False, index=True)

    habit = relationship("Habit", back_populates="habit_track")

    def __str__(self) -> str:
        return (
            f"id привычки: {self.habit_id}\nДата выполнения: {dt.strftime(self.date_of_completion, '%d-%m-%Y')}"
            f"\nПривычка в этот день выполнена? {'Да' if self.is_done else 'Нет'}"
        )
