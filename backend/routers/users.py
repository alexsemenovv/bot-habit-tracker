from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.future import select

from utils import get_session
from schemas.user_schemas import UserIn, UserOut
from databases.models import User

router = APIRouter(prefix='/api/users')


@router.post("", response_model=UserOut)
async def add_user(user: UserIn, session=Depends(get_session)) -> User:
    """Добавление нового пользователя"""
    new_user: User = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user


@router.get("", response_model=List[UserOut])
async def get_users(session=Depends(get_session)) -> List[User]:
    """Получение списка всех пользователей"""
    res = await session.execute(select(User))
    return res.scalars().all()
