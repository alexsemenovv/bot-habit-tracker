from typing import List, Optional

from fastapi import APIRouter, Depends, Path
from sqlalchemy.future import select

from databases.models import User
from schemas.user_schemas import UserIn, UserOut
from utils import get_session

router = APIRouter(prefix="/api/users")


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


@router.get("/{tg_id}", response_model=Optional[UserOut])
async def get_user_by_tg_id(
    tg_id: int = Path(..., description="Telegram id пользователя"),
    session=Depends(get_session),
) -> User:
    """Получение пользователя по tg id"""
    res = await session.execute(select(User).where(tg_id == User.tg_id))
    return res.scalars().first()
