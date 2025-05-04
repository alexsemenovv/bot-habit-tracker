from typing import AsyncGenerator

from databases.database import Base, async_session, engine


async def get_session() -> AsyncGenerator:
    """Создание генератора сессии"""
    async with async_session.begin() as session:
        yield session


async def create_tables():
    """Создание таблиц перед"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Удаление всех таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
