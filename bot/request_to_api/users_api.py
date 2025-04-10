import json
from typing import Dict

import requests

API_URL = "http://127.0.0.1:8000/api/users"  # Адрес FastAPI


def get_user_by_tg_id(tg_id: int) -> bool:
    """Получение user по tg_id."""
    response = requests.get(f'{API_URL}/{tg_id}')
    # Парсим JSON-ответ
    data = response.json()
    if data is None:
        return False  # пользователя нет
    return True  # пользователь есть


def add_user_with_api(user_data: Dict):
    """Добавление пользователя в БД"""

    # Преобразуем словарь в json
    data = json.dumps(user_data)
    response = requests.post(API_URL, data=data) # делаем запрос к endpoint на добавление пользователя
    if response.status_code == 200:
        return True
    return False
