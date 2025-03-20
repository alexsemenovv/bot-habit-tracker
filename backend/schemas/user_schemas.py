from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    """Базовая схема пользователя"""
    first_name: str
    last_name: Optional[str] = None
    username: str
    tg_id: int
    is_bot: bool


class UserIn(BaseUser):
    """Схема 'пользователь' на вход"""
    ...


class UserOut(BaseUser):
    """Схема 'пользователь' на выход"""
    id: int

    model_config = {
        "from_attributes": True
    }
