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
    is_active = Column(Boolean, nullable=True, default=True, index=True)

    user = relationship("User", back_populates="habits")

    def __str__(self) -> str:
        return f"Привычка: {self.name}\nДата начала: {dt.strftime(self.start_date, '%d-%m-%Y')}"
