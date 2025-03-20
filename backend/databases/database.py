from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base


DATABASE_URL = 'sqlite+aiosqlite:///databases/habits.db'

engine = create_async_engine(url=DATABASE_URL)  # , echo=True) вкл/выкл логов дб

async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()