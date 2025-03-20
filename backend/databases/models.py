from datetime import datetime as dt

from sqlalchemy import Column, VARCHAR, Integer, Text, Date

from database import Base


class Habit(Base):
    __tablename__ = "Habit"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(50), index=True, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False, default=dt.date(dt.now()))
